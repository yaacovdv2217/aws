#!/usr/bin/env python3
import boto3


def validate_selection(
        selection, possible_values, decrease_num=False, accept_blank=False
):
    possible_selections = possible_values
    if isinstance(possible_values, dict):
        is_dict = True
        possible_selections = [i for i in possible_values]
    try:
        int(selection)
        isNum = True
    except ValueError:
        isNum = False

    if isNum:
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

session = boto3.Session(profile_name=selected_profile)
main_client = session.client("ec2", region_name="us-east-1")

# iterate on all regions
for region in main_client.describe_regions()["Regions"]:
    region_name = region["RegionName"]
    print("||| Region {} |||".format(region_name))
    client = session.client("ec2", region_name=region_name)
    all_instances = client.describe_instances()
    if len(all_instances["Reservations"]) == 0:
        continue

    num_of_instances = all_instances["Reservations"][0]["Instances"][0]["InstanceId"]
    print(num_of_instances)
    # if num_of_instances > 0:
    #     print(
    #         "||| {} instances in region {} |||".format(
    #             num_of_instances, region_name
    #         )
    #     )
