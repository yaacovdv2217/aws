import boto3
from pprint import pprint


# global variables

selected_profile = get_user_input(boto3.session.Session().available_profiles)
session = boto3.Session(profile_name=selected_profile)

for acct in accounts:
       session = boto3.Session(profile_name=acct)
       iam = session.client('iam')
       for user in usernames:
           iam.create_user(UserName=user)


client = boto3.client('ec2', 'Regions')
for each_inst in client.describe_instances()['Reservations']:
    for inst_id in each_inst['Instances']:
        for region in client.describe_regions()["Regions"]:
            region_name = region["RegionName"]
        pprint(inst_id['InstanceId'])
