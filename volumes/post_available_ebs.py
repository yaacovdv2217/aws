import requests
import boto3
from datetime import datetime
import os
from decouple import config

# Slack Webhook URL
SLACK_URL = config("SLACK_URL")

# Global Variables
regions_dict = {}


# Function to select profile
def select_profile(options):
    for i, k in enumerate(options):
        print(f"{i + 1}) {k}")
    selection = input("Enter selection: ")
    try:
        index = int(selection) - 1
        if index >= 0 and index < len(options):
            return options[index]
    except ValueError:
        pass
    return None


# Function to get unused EBS in a region
def get_unused_ebs(region):
    client = boto3.resource("ec2", region_name=region)
    volumes = []
    for volume in client.volumes.filter(
            Filters=[{"Name": "status", "Values": ["available"]}]
    ):
        if volume.state == "available":
            volume_id = volume.id
            if volume.tags:
                volume_name = next((tag['Value'] for tag in volume.tags if tag['Key'] == 'Name'), '<No Name Tag>')
            else:
                volume_name = '<No Name Tag>'
            volumes.append({'id': volume_id, 'name': volume_name})
    return volumes


# Function to get all unused EBS in all regions
def get_unused_ebs_all_regions():
    unused_all_regions = {}
    client = boto3.client("ec2")
    dict_of_regions = client.describe_regions()
    for item in dict_of_regions["Regions"]:
        region = item["RegionName"]
        unused_ebs = get_unused_ebs(region)
        if unused_ebs:
            unused_all_regions[region] = unused_ebs
    return unused_all_regions


# Function to format the message
def format_message(profile, data):
    message = f"_Here are the available EBS in all regions for Account: `{profile}`:_\n"
    for region, volumes in data.items():
        message += f"\n_Region: `{region}`_\n"
        for volume in volumes:
            message += "```\n"
            message += f"Volume ID: {volume['id']}\n"
            if volume['name']:
                message += f"Volume Name: {volume['name']}\n"
            message += "```\n"
    return message


# Function to send slack message
def send_slack_message(message):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "text": message
    }
    response = requests.post(SLACK_URL, headers=headers, json=payload)
    return response.text


# Main function
def main():
    profile = select_profile(boto3.session.Session().available_profiles)
    boto3.setup_default_session(profile_name=profile)
    data = get_unused_ebs_all_regions()
    message = format_message(profile, data)
    send_slack_message(message)


if __name__ == "__main__":
    main()
