import boto3
import requests

GLOBAL_REGIONS_DICT = {}


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


def available_regions():
    service: str = "ec2"
    regions: list = []
    client = boto3.client(service)
    dict_of_regions = client.describe_regions()
    for item in dict_of_regions["Regions"]:
        regions.append(item["RegionName"])
        GLOBAL_REGIONS_DICT[item["RegionName"]] = []
    return regions


def get_user_input(options):
    for i, k in enumerate(options):
        print("{} ) {}".format(str(i + 1), k))
    selection = input("Enter selection: ")
    final_selection = validate_selection(selection, options, True)
    while not final_selection:
        selection = input("Enter selection: ")
        final_selection = validate_selection(selection, options, True)
        # for j, d in enumerate(options):
        #     print("{} ) {}".format(str(j + 1), d))
        # regions: list = available_regions()
        # region_selection = input("Choose a Region: ")
        # final_region_selection = validate_selection(region_selection, options, True)
        # while not final_region_selection:
        #     region_selection = input("Choose a Region: ")
        #     final_region_selection = (validate_selection(region_selection, regions, options, True))
        #     return final_region_selection

    return final_selection


selected_profile = get_user_input(boto3.session.Session().available_profiles)
session = boto3.setup_default_session(profile_name=selected_profile)


def create_volume():
    regional_client = boto3.client("ec2", region_name=selected_profile)
    new_volume = regional_client.crerate_volume(
        AvailabilityZone=f"{selected_profile}",
        Size=10,
        VolumeType='gp2',
        TagSpecifications=[
            {
                'ResourceType': 'volume',
                'Tags': [{'Key': 'yaacov', 'Value': 'yaacov_test3'}]}])
    print(f'Created Volume ID: {new_volume["VolumeId"]}')
    return new_volume
