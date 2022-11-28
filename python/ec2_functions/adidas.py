import json
import boto3
import requests
from botocore.config import Config
from datetime import datetime
import requests

#global variables
current_date = datetime.today().strftime('%Y-%m-%d')
time_current_date = datetime.strptime(current_date, "%Y-%m-%d")
status_check = "running"
global_instances_dict: dict = {}
instances_to_terminate: dict = {}


def check_if_creator_exist_and_update(list_of_tags):
    creator_value = None
    for list_operator_is_dict in list_of_tags:
        if "creator" in list_operator_is_dict.values():
            creator_value = list_operator_is_dict["Value"]
    return creator_value


def check_if_date_exist_and_update(list_of_tags):
    date_value = None
    for list_operator_is_dict in list_of_tags:
        if "date" in list_operator_is_dict.values():
            date_value = list_operator_is_dict["Value"]
    return date_value


def available_regions(service):
    regions: list = []
    adi_client = boto3.client(service)
    dict_of_regions = adi_client.describe_regions()
    for item in dict_of_regions["Regions"]:
        regions.append(item["RegionName"])
        global_instances_dict[item["RegionName"]] = []
        instances_to_terminate[item["RegionName"]] = []
    return regions


def validate_tags(list_of_dictionaries):
    if list_of_dictionaries[0]['creator'] is None:
        return False
    if list_of_dictionaries[1]['date'] is None:
        return False
    try:
        t_tag = datetime.strptime(list_of_dictionaries[1]['date'], "%y-%m-%d")
    except Exception as e:
        if list_of_dictionaries[1]['date'] == "NEVER":
            return True
        else:
            return False

    if time_current_date > t_tag:
        return False
    return True


def check_if_should_terminate_instances():
  for region in global_instances_dict:
       if global_instances_dict[region]:
            handle_instance_list_validation(global_instances_dict[region],region)


def handle_instance_list_validation(list_of_instances_dict,region):
    for instance_dict in list_of_instances_dict:
        msg_in_case_valid = None
        bool_var = validate_tags(instance_dict["tags"])
        if (not bool_var) and (instance_dict["status"] == "running"):
            instances_to_terminate[region].append(instance_dict)
        if bool_var:
            msg_in_case_valid = """
`{0}`,
`{1}`,
`{2}`
             """.format(instance_dict["tags"][0]["creator"], instance_dict["tags"][1]["date"],instance_dict["id"])
            if instance_dict["status"] != "terminated":
                slack_message(msg_in_case_valid,None,"https://hooks.slack.com/services/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")



def slack_message(message_text=None, payload_obj=None, slack_url=None):
    if (not slack_url):
       slack_url = "https://hooks.slack.com/services/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"
    if (not payload_obj and message_text):
        payload_obj = {"text": "\n" +str(message_text) + "\n", "username": "NOT TERMINATING","link_names": 1,"icon_emoji": ":monkey:"}
    r = requests.put(slack_url, data=json.dumps(payload_obj))


def find_unnecessary_instances_aws():
    counter_instances_all: int = 0
    print(f"Check for status: {status_check}")
    service: str = 'ec2'
    region_list: list = available_regions(service)
    print(region_list)
    for specific_region in region_list:
        print(f"Starting work on {specific_region}!!!")
        counter_instances: int = 0
        reservation_dictionary_per_region_response = get_instances_per_region_reservation(service, specific_region)
        for instance_dict in reservation_dictionary_per_region_response["Reservations"]:
            update_global_dict(instance_dict, specific_region)
            counter_instances += 1
            counter_instances_all += 1
        if counter_instances == 1:
            print(f"In {specific_region} running {counter_instances} instance")
        elif counter_instances == 0:
            print(f" In {specific_region}, there aro no running instances")
        else:
            print(f" In {specific_region} {counter_instances}  instances are running")
        counter_instances = 0
    print(f" In all regions currently running {counter_instances_all} instances")


def get_instances_per_region_reservation(service, specific_region):
    adi_config = Config(region_name=specific_region)
    client = boto3.client(service, config=adi_config)
    dictionary_per_region_response = client.describe_instances()
    return dictionary_per_region_response


def terminate_instances():
    response_termination = None
    service = "ec2"
    for region in instances_to_terminate:
        try:
            ec2 = boto3.client(service,region)
            response_termination = ec2.terminate_instances(InstanceIds=list_of_instances_to_terminate(region))
        except Exception as e:
                print(e)
        if response_termination:
            response_termination_final = {}
            response_termination_final["region"] = region
            for small_message in response_termination['TerminatingInstances']:
                small_message_key= small_message['InstanceId']
                small_message_value = small_message['CurrentState']['Name']
                response_termination_final[small_message_key] = small_message_value

            payload_obj = {"text": "```\n" + str(response_termination_final) + "\n```", "username": "TERMINATING INSTANCES", "link_names": 1,
                               "icon_emoji": ":gun:"}
            if response_termination != "":
                slack_message(None, payload_obj=payload_obj, slack_url="https://hooks.slack.com/services/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")
                payload_obj = {}
            response_termination = ""

def list_of_instances_to_terminate(region):
    response_list = []
    for instance_dict in instances_to_terminate[region]:
        response_list.append(instance_dict["id"])
    return response_list


def update_global_dict(instance_dict, region):
    instance_dictionary = {}
    instance_dictionary["id"] = instance_dict["Instances"][0]["InstanceId"]
    instance_dictionary["status"] = instance_dict["Instances"][0]["State"]["Name"]
    instance_dictionary["instance_type"] = instance_dict["Instances"][0]["InstanceType"]
    try:
        instance_dictionary["tags"] = [{"creator" : check_if_creator_exist_and_update(instance_dict["Instances"][0]["Tags"])}, {"date": check_if_date_exist_and_update(instance_dict["Instances"][0]["Tags"])}]
    except Exception as e:
        instance_dictionary["tags"] = [{"creator": None}, {"date": None}]
    instance_dictionary["BlockDeviceMappings"] = instance_dict["Instances"][0]["BlockDeviceMappings"]
    if "InstanceLifecycle" in instance_dict["Instances"][0]:
         instance_dictionary["InstanceLifecycle"] = instance_dict["Instances"][0]["InstanceLifecycle"]
    else:
        instance_dictionary["InstanceLifecycle"] = "On-Demand"
    global_instances_dict[region].append(instance_dictionary)


if __name__ == "__main__":
    accountId = "act-eccf5eae"
    internalAccessToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzcG90aW5zdCIsImV4cCI6MTg5NzIyMjY1NiwiaWF0IjoxNTgxODYyNjU2LCJ1aWQiOi0xLCJyb2xlIjoyLCJvaWQiOiI2MDYwNzk4NzUwMTAifQ.B7n7iz8BBXleSZVdxodTGWCTK8PhRH92NfYmXdiDPfs"
    find_unnecessary_instances_aws()
    for region, list_of_instances_dict in global_instances_dict.items():
        for i in list_of_instances_dict:
            print(region, " : ", i)
    check_if_should_terminate_instances()
    terminate_instances()
    print("We are so close")