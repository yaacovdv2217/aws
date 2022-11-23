import boto3
from datetime import datetime
import requests

GLOBAL_REGIONS_DICT: dict = {}
CURRENT_DATE = datetime.today().strftime("%Y-%m-%d")
TIME_CURRENT_DATE = datetime.strptime(CURRENT_DATE, "%Y-%m-%d")



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


selected_profile = get_user_input(boto3.session.Session().available_profiles)
session = boto3.setup_default_session(profile_name=selected_profile)


# 0.08 per GB-month * 2,000 GB * 43,200 seconds / (86,400 seconds/day * 30-day month))

# def hourly_cost():
#     service: str = "ec2"
#     client = boto3.client(service)
#     dict_of_volumes = client.describe_volumes()
#     # gp2 = (0.1 * volume.size / (720 * 30))
#     # io2 = (0.125 * volume.size / (720 * 30))
#     # gp3 = (0.08 * volume.size / (720 * 30))
#     # sc1 = (0.015 * volume.size / (720 * 30))
#     hourly_charge = []
#     for volume in dict_of_volumes.volumes.all():
#         volume_id = volume.id
#         volume_size = volume.size
#         volume_type = volume.volume_type
#         hourly_charge.append(volume_size)
#         hourly_charge.append(volume_id)
#         hourly_charge.append(volume_type)
#         print("ID:", volume.id, "|", "Type:", volume.volume_type, "|", "Size:", volume.size, "GIB", "|", "Iops:",
#               volume.iops,
#               "|", "Throughput:", volume.throughput, "|", "Hourly Cost:", volume_type * volume_size / (720 * 30))
#
#     return hourly_charge


def list_of_profiles():
    all_profiles: list = []
    for profile in boto3.session.Session().available_profiles:
        all_profiles.append(profile)
    return all_profiles


def ebs_list_parameters(region):
    regional_client = boto3.resource("ec2", region_name=region)
    gp3 = 0.08
    gp2 = 0.1
    io2 = 0.125
    sc1 = 0.015
    volumes = []
    for volume in regional_client.volumes.all():
        volume_id = volume.id
        volumes.append(volume_id)
        if volume.volume_type == int(gp3) or int(gp2) or int(io2) or int(sc1):
            return volume.volume_type
        # volumes.append(volume_id["VolumeType", "Iops", "Size", "VolumeId"])

        # GLOBAL_VOLUME_DICT[volume["VolumeType", "Iops", "Size", "VolumeId"]] = []
        # hourly_charge = int(volume.size * volume.volume_type) / (720 * 30)

        print(f"ID:", volume.id, "|", "Type:", volume.volume_type, "|", "Size:", volume.size, "GIB", "|", "Iops:",
              volume.iops,
              "|", "Throughput:", volume.throughput, "|", "Hourly Cost:", volume.volume_type * volume.size)

    return volumes


def available_regions():
    service: str = "ec2"
    regions: list = []
    client = boto3.client(service)
    dict_of_regions = client.describe_regions()
    for item in dict_of_regions["Regions"]:
        regions.append(item["RegionName"])
        GLOBAL_REGIONS_DICT[item["RegionName"]] = []
    return regions


def describe_disks_in_all_regions():
    all_unused_all_regions = {}
    region_list: list = available_regions()
    for specific_region in region_list:
        print(f"Checking  region {specific_region}")
        ebs_list: list = ebs_list_parameters(specific_region)
        if len(ebs_list) > 0:
            all_unused_all_regions[specific_region] = ebs_list
            print("")
        else:
            print("No available Volumes")
    return all_unused_all_regions


def nice_format_message(unused_ebs_dictionary):
    message = ""
    for region, volumes in unused_ebs_dictionary.items():
        message += "\n"
        for volume in volumes:
            message += f"{volume}\n"
    return message


def format_message(unused_ebs_dict):
    message = f"*All EBS Volumes in {selected_profile}*\n"
    for region, volumes in unused_ebs_dict.items():
        message += f"*{region}*\n"
        for volume in volumes:
            message += f"{volume}\n"
    return message


def send_message(message):
    slack_url = "https://hooks.slack.com/services/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"
    payload_obj1 = '{"text": "%s"}' % message
    response = requests.post(slack_url, payload_obj1)
    return response.text


def main():
    message = format_message(describe_disks_in_all_regions())
    send_message(message=message)


main()
# def ebs_pricing():
#     for ebs_code in ebs_name_map:
#         response = pricing_auth.get_products(ServiceCode='AmazonEC2', Filters=[
#             {'Type': 'TERM_MATCH', 'Field': 'volumeType', 'Value': ebs_name_map[ebs_code]},
#             {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region}])
#         for result in response['PriceList']:
#             json_result = json.loads(result)
#             for json_result_level_1 in json_result['terms']['OnDemand'].values():
#                 for json_result_level_2 in json_result_level_1['priceDimensions'].values():
#                     for price_value in json_result_level_2['pricePerUnit'].values():
#                         continue
#         ebs_name_map[ebs_code] = float(price_value)
#     return ebs_name_map
