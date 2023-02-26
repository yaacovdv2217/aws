import requests
import boto3
from decouple import config


def describe_disks_in_all_regions():
    unused_ebs_dict = {}
    region_list: list = available_regions()
    for specific_region in region_list:
        ebs_list: list = ebs_list_parameters(specific_region)
        if len(ebs_list) > 0:
            unused_ebs_dict[specific_region] = ebs_list
    return unused_ebs_dict


def nice_format_message(unused_ebs_dictionary):
    message = ""
    for region, volumes in unused_ebs_dictionary.items():
        message += f"{region}:\n"
        for volume in volumes:
            message += f"```{volume}```\n"
    return message


def format_message(unused_ebs_dict):
    message = f"*All EBS Volumes in {profile}*\n"
    for region, volumes in unused_ebs_dict.items():
        message += f"*{region}*\n"
        for volume in volumes:
            message += f"```{volume}```\n"
    return message


def send_message(message):
    slack_url = config("SLACK_URL")
    response = requests.post(slack_url, json={"text": message}, headers={"Content-type": "application/json"})
    return response.text


def main():
    message = format_message(describe_disks_in_all_regions())
    send_message(message)


def select_profile(profiles):
    if len(profiles) == 1:
        return profiles[0]
    else:
        for i, profile in enumerate(profiles):
            print(f"{i+1}: {profile}")
        selected_profile = input("Select the profile number: ")
        return profiles[int(selected_profile)-1]


def available_regions():
    ec2 = boto3.client('ec2')
    response = ec2.describe_regions()
    return [region['RegionName'] for region in response['Regions']]


def ebs_list_parameters(region):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    volumes = []
    for volume in response['Volumes']:
        volume_id = volume['VolumeId']
        size = volume['Size']
        availability_zone = volume['AvailabilityZone']
        volume_type = volume['VolumeType']
        volumes.append(f"Volume ID: {volume_id}\nSize: {size} GB\nAvailability Zone: {availability_zone}\nVolume Type: {volume_type}")
    return volumes


if __name__ == '__main__':
    profile = select_profile(boto3.session.Session().available_profiles)
    boto3.setup_default_session(profile_name=profile)
    main()
