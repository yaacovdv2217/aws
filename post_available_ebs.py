import requests
import boto3
from datetime import datetime
import os
from decouple import config
import schedule
import time

# Global Variables
GLOBAL_REGIONS_DICT: dict = {}
CURRENT_DATE = datetime.today().strftime("%Y-%m-%d")
TIME_CURRENT_DATE = datetime.strptime(CURRENT_DATE, "%Y-%m-%d")


# _____________________________________________________________________________
# Function to call for a Profile account
# _____________________________________________________________________________
def validate_selection(
        selection, possible_values, decrease_num=False, accept_blank=False
):
    possible_selections = possible_values
    if isinstance(possible_values, dict):
        is_dict = True
        possible_selections = [i for i in possible_values]
    try:
        int(selection)
        is_number = True
    except ValueError:
        is_number = False

    if is_number:
        check_num = int(selection)
        if decrease_num:
            check_num = check_num - 1

        if check_num < len(possible_selections):
            return possible_selections[check_num]
        else:
            return False
    else:
        if accept_blank and selection == "":
            return True
        if selection in possible_selections:
            return selection
        else:
            return False


def get_user_input(options):
    for i, k in enumerate(options):
        print("{} ) {}".format(str(i + 1), k))
    selection = input("Enter selection: ")
    final_selection = validate_selection(selection, options, True)
    while not final_selection:
        selection = input("Enter selection: ")
        final_selection = validate_selection(selection, options, True)
    return final_selection


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


# ______________________________________________________________
# Format Message for printing nice - for nice printing in Terminal
# ______________________________________________________________
def nice_format_message(unused_ebs_dictionary):
    message = ""
    for region, volumes in unused_ebs_dictionary.items():
        message += "\n"
        for volume in volumes:
            message += f"{volume}\n"
    return message


# _______________________________________________________________
# Function to call Unused EBS In All_Regions
# _______________________________________________________________
def describe_unused_ebs_in_all_regions():
    all_unused_all_regions = {}
    region_list: list = available_regions()
    for specific_region in region_list:
        print(f"Checking  region {specific_region}")
        ebs_list: list = describe_unused_ebs(specific_region)
        if len(ebs_list) > 0:
            all_unused_all_regions[specific_region] = ebs_list
            print(nice_format_message(all_unused_all_regions))
        else:
            print("No available Volumes")
    return all_unused_all_regions


def create_snapshot_for_available_ebs():
    # create a dictionary of snapshots with their snapshot ids which were created successfully
    successful_snapshots = dict()
    volume_dict: dict = describe_unused_ebs_in_all_regions()
    regional_client = boto3.resource("ec2", "region-name")
    # iterate through each item in volumes_dict and use key as description of snapshot
    for snapshot in volume_dict:
        try:
            response = regional_client.create_snapshot(
                Description=snapshot,
                VolumeId=volume_dict[snapshot],
                DryRun=False
            )
            # response is a dictionary containing ResponseMetadata and SnapshotId
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            snapshot_id = response['SnapshotId']
            # check if status_code was 200 or not to ensure the snapshot was created successfully
            if status_code == 200:
                successful_snapshots[snapshot] = snapshot_id
        except Exception as e:
            exception_message = "There was error in creating snapshot " + snapshot + \
                                " with volume id ", str(volume_dict[snapshot]), " and error is: \n" \
                                + str(e)
            print(successful_snapshots)
    # print the snapshots which were created successfully
    return successful_snapshots


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
    message = f"*Unused EBS Volumes in {selected_profile}*\n"
    for region, volumes in unused_ebs_dict.items():
        message += f"*{region}*\n"
        for volume in volumes:
            message += f"{volume}\n"
    return message


# _________________________________________________________________
# Call Slack
# _________________________________________________________________
def send_message(message):
    slack_url = config('SLACK_URL')
    payload_obj1 = '{"text": "%s"}' % message
    response = requests.post(slack_url, payload_obj1)
    return response.text


# _______________________________________________________________
# Function to call Schedule Time
# _______________________________________________________________
def main():
    message = format_message(describe_unused_ebs_in_all_regions())
    print(send_message(message=message))


if __name__ == "__main__":
    selected_profile = get_user_input(boto3.session.Session().available_profiles)
    session = boto3.setup_default_session(profile_name=selected_profile)
    # schedule.every().day.at("12:15").do(schedule_time_list_unused_ebs)
main()
# while True:
#     schedule.run_pending()
#     time.sleep(1)
