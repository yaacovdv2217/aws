import json

import boto3
from datetime import datetime

PROFILE_NAME = 'devops-labs'
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
    return json.dumps(all_unused_all_regions)


print(describe_unused_ebs_in_all_regions())

# volume_dict = json.dumps(describe_unused_ebs_in_all_regions())
# listToStr = ' '.join([str(elem) for elem in describe_unused_ebs_in_all_regions()])
# print(listToStr)

# successful_snapshots = dict()
# regional_client = boto3.resource("ec2", "us-west-2")
# for snapshot in volume_dict:
#     try:
#         response = regional_client.create_snapshot(
#             Description=snapshot,
#             VolumeId=volume_dict[snapshot],
#             DryRun=False
#         )
#         # response is a dictionary containing ResponseMetadata and SnapshotId
#         status_code = response['ResponseMetadata']['HTTPStatusCode']
#         snapshot_id = response['SnapshotId']
#         # check if status_code was 200 or not to ensure the snapshot was created successfully
#         if status_code == 200:
#             successful_snapshots[snapshot] = snapshot_id
#     except Exception as e:
#         exception_message = "There was error in creating snapshot " + snapshot + \
#                             " with volume id ", volume_dict[snapshot], " and error is: \n" \
#                             + str(e)
# print(successful_snapshots)

# VOLUME_ID = volume_dict
# AWS_REGION = "us-west-2"
# regional_client = boto3.resource("ec2", region_name=AWS_REGION)
# snapshot = regional_client.create_snapshot(
#     VolumeId=VOLUME_ID,
#     TagSpecifications=[
#         {
#             'ResourceType': 'snapshot',
#             'Tags': [
#                 {
#                     'Key': 'Name',
#                     'Value': 'my-snapshot'
#                 },
#             ]
#         },
#     ]
# )
# print(f"Snapshot{snapshot.id} Created for Volume{VOLUME_ID}")
