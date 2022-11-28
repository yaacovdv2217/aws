import requests
import boto3
from datetime import datetime
import schedule
import time

# Global Variables
PROFILE_NAME = 'big-data'
boto3.setup_default_session(profile_name=PROFILE_NAME)
GLOBAL_REGIONS_DICT: dict = {}
CURRENT_DATE = datetime.today().strftime("%Y-%m-%d")
TIME_CURRENT_DATE = datetime.strptime(CURRENT_DATE, "%Y-%m-%d")


# def validate_selection(
#         selection, possible_values, decrease_num=False, accept_blank=False
# ):
#     possible_selections = possible_values
#     if isinstance(possible_values, dict):
#         is_dict = True
#         possible_selections = [i for i in possible_values]
#     try:
#         int(selection)
#         is_number = True
#     except ValueError:
#         is_number = False
#
#     if is_number:
#         check_num = int(selection)
#         if decrease_num:
#             check_num = check_num - 1
#
#         if check_num < len(possible_selections):
#             return possible_selections[check_num]
#         else:
#             return False
#     else:
#         if accept_blank and selection == "":
#             return True
#         if selection in possible_selections:
#             return selection
#         else:
#             return False
#
#
# def get_user_input(options):
#     for i, k in enumerate(options):
#         print("{} ) {}".format(str(i + 1), k))
#     selection = input("Enter selection: ")
#     final_selection = validate_selection(selection, options, True)
#     while not final_selection:
#         selection = input("Enter selection: ")
#         final_selection = validate_selection(selection, options, True)
#     return final_selection


# selected_profile = get_user_input(boto3.session.Session().available_profiles)
# session = boto3.Session(profile_name=selected_profile)
# main_client = session.client("ec2", region_name="us-east-1")


# block = {
#     "blocks": [
#         {
#             "type": "section",
#             "text": {
#                 "type": "mrkdwn",
#                 "text": "*Do you approve? \n*"
#             }
#         },
#         {
#             "type": "actions",
#             "elements": [
#                 {
#                     "type": "button",
#                     "text": {
#                         "type": "plain_text",
#                         "emoji": True,
#                         "text": "Approve"
#                     },
#                     "style": "primary",
#                     "value": "click_me_123"
#                 },
#                 {
#                     "type": "button",
#                     "text": {
#                         "type": "plain_text",
#                         "emoji": True,
#                         "text": "Deny"
#                     },
#                     "style": "danger",
#                     "value": "click_me_123"
#                 }
#             ]
#         }
#     ]
# }

# _______________________________________________________________
# Function to call Unused EBS
# _______________________________________________________________
def describe_unused_ebs(region):
    regional_client = boto3.resource("ec2", region_name=region)
    volumes = []
    for volume in regional_client.volumes.filter(
            Filters=[{"Name": "status", "Values": ["available"]}]
    ):
        if volume.state == "available":
            volume_id = volume.id
            volumes.append(volume_id)
    return volumes


# ________________________________________________________________
# Function to call All Regions
# ________________________________________________________________
def available_regions():
    service: str = "ec2"
    regions: list = []
    client = boto3.client(service)
    dict_of_regions = client.describe_regions()
    for item in dict_of_regions["Regions"]:
        regions.append(item["RegionName"])
        GLOBAL_REGIONS_DICT[item["RegionName"]] = []
    return regions


# _______________________________________________________________
# function to call list of Profiles
# _______________________________________________________________
def list_of_profiles():
    all_profiles: list = []
    for profile in boto3.session.Session().available_profiles:
        all_profiles.append(profile)
    return all_profiles


# _______________________________________________________________
# Function to call Unused EBS In All_Regions
# _______________________________________________________________
def describe_unused_ebs_in_all_regions():
    all_unused_all_regions = {}
    # profile_list: list = list_of_profiles()
    region_list: list = available_regions()
    # for specific_profile in profile_list:
    #     print(f"profile name: *{specific_profile}*")
    #     region_in_profile: list = available_regions()
    #     if len(region_in_profile) > 0:
    #         all_unused_all_regions[specific_profile] = region_in_profile
    for specific_region in region_list:
        print(f"Checking  region {specific_region}")
        ebs_list: list = describe_unused_ebs(specific_region)
        if len(ebs_list) > 0:
            all_unused_all_regions[specific_region] = ebs_list
    return all_unused_all_regions


# ____________________________________________________________________
# Functions to call to start Deleting:
# ____________________________________________________________________
# volume_dict = {describe_unused_ebs_in_all_regions()}
def delete_unused_ebs(region):
    regional_client = boto3.resource("ec2", region_name=region)
    volumes = []
    for volume in regional_client.volumes.filter(
            Filters=[{"Name": "status", "Values": ["available"]}]
    ):
        if volume.state == "available":
            volume_id = volume.id
            volumes.append(volume_id)
            volume.delete()
    return volumes


# _________________________________________________________________
# Combine Unused Volumes in All Regions
# _________________________________________________________________
def delete_ebs_in_all_regions():
    all_unused_all_regions = {}
    region_list: list = available_regions()
    for specific_region in region_list:
        print(f"Checking  region {specific_region}")
        ebs_list: list = delete_unused_ebs(specific_region)
        if len(ebs_list) > 0:
            all_unused_all_regions[specific_region] = ebs_list
    return all_unused_all_regions


# __________________________________________________________________
# Format message
# __________________________________________________________________
# accept dictionary that looks like:
# {"us-east-1": ["vol-123", "vol-456"], "us-west-2": ["vol-789"]}
# output:
# """
# *Unused EBS Volumes*
# *us-east-1*
# vol-123
# vol-456
# *us-west-2*
# vol-789
# """
def format_message(unused_ebs_dict):
    message = f"*Unused EBS Volumes in Accounts*\n"
    for region, volumes in unused_ebs_dict.items():
        message += f"*{region}*\n"
        for volume in volumes:
            message += f"{volume}\n"
    return message


# _________________________________________________________________
# Call Slack
# _________________________________________________________________
def send_message(message):
    slack_url = "https://hooks.slack.com/services/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"
    payload_obj1 = '{"text": "%s"}' % message
    response = requests.post(slack_url, payload_obj1)
    return response.text


# _______________________________________________________________
# Function to call Schedule
# _______________________________________________________________
def schedule_time_list_unused_ebs():
    message = format_message(describe_unused_ebs_in_all_regions())
    print(send_message(message=message))


schedule_time_list_unused_ebs()

# if __name__ == "__main__":
#     schedule.every().day.at("11:11").do(schedule_time_list_unused_ebs)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
