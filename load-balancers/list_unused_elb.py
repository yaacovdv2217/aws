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


# Function to get unused ALBs in a region
# Function to get unused ALBs in a region
def find_unused_elbs(region):
    elb_client = boto3.client('elb', region_name=region)
    unused_elbs = []
    response = elb_client.describe_load_balancers()
    for load_balancer in response['LoadBalancerDescriptions']:
        instances = elb_client.describe_instance_health(LoadBalancerName=load_balancer['LoadBalancerName'])
        if len(instances['InstanceStates']) == 0:
            unused_elbs.append(load_balancer['LoadBalancerName'])
    return unused_elbs


# Function to get all unused ALBs in all regions
def get_unused_elb_all_regions():
    unused_all_regions = {}
    elb_client = boto3.client('elbv2')
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    for region in regions:
        unused_elb = find_unused_elbs(region)
        if unused_elb:
            unused_all_regions[region] = unused_elb
    return unused_all_regions


def format_message(profile, data):
    message = f"Here are the ALBs that have no instances attached in all availability zones for account: `{profile}`:\n\n"
    if not data:
        message += "No unused ALBs found in any region."
    else:
        for region, elbs in data.items():
            if not elbs:
                message += f"`No unused ALBs found in {region}.`\n\n"
            else:
                message += f"`Unused ALBs in {region}:`\n"
                for elb in elbs:
                    message += f"```{elb}```\n"
                message += "\n"
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
    data = get_unused_elb_all_regions()
    message = format_message(profile, data)
    send_slack_message(message)


if __name__ == "__main__":
    main()
