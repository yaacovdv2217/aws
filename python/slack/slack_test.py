import requests
import boto3
from datetime import datetime
import schedule
import time

# Global Variables
boto3.setup_default_session(profile_name='spotinst-automation')
global_regions_dict: dict = {}
current_date = datetime.today().strftime('%Y-%m-%d')
time_current_date = datetime.strptime(current_date, "%Y-%m-%d")
schedule = schedule_time()

# Function to call Unused EBS
def unused_ebs(region):
    regional_client = boto3.resource('ec2', region_name=region)
    volumes = []
    for volume in regional_client.volumes.filter(
            Filters=[{'Name': 'status', 'Values': ['available']}]):
        if volume.state == "available":
            volume_id = volume.id
            volumes.append({"id": volume_id, "region": region})
    return volumes


# Function to call All Regions
def available_regions():
    service: str = 'ec2'
    regions: list = []
    client = boto3.client(service)
    dict_of_regions = client.describe_regions()
    for item in dict_of_regions["Regions"]:
        regions.append(item["RegionName"])
        global_regions_dict[item["RegionName"]] = []
    return regions


# Function to call Unused EBS In All_Regions
def unused_ebs_in_all_regions():
    all_unused_all_regions = []
    region_list: list = available_regions()
    for specific_region in region_list:
        print(f"Checking  region {specific_region}")
        ebs_list: list = unused_ebs(specific_region)
        if len(ebs_list) > 0:
            all_unused_all_regions.append(ebs_list)
    return all_unused_all_regions


# print(unused_ebs_in_all_regions())


# Function to call Schedule
def schedule_time():
    schedule.every(5).seconds.do(schedule_time)
    schedule.run_pending()
    time.sleep(5)
    return unused_ebs_in_all_regions()
    # return unused_ebs(), available_regions()


# Call Slack
def send_message(message):
    slack_url = "https://hooks.slack.com/services/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"
    payload_obj = '{"text": "%s", "icon_emoji": ":monkey:"}' % message
    response = requests.post(slack_url, payload_obj)
    return response.text


print(send_message(message=f"*Unused EBS:* " "\n" + str(schedule_time())))
# print(send_message(message=(schedule_time())))
