import boto3
from datetime import datetime

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


def available_regions():
    service: str = "ec2"
    regions: list = []
    client = boto3.client(service)
    dict_of_regions = client.describe_regions()
    for item in dict_of_regions["Regions"]:
        regions.append(item["RegionName"])
        GLOBAL_REGIONS_DICT[item["RegionName"]] = []
    return regions


def describe_unused_ebs(region):
    regional_client = boto3.resource("ec2", region_name=region)
    volumes = []
    for volume in regional_client.volumes.filter(
            Filters=[{"Name": "status", "Values": ["in-use"]}]
    ):
        if volume.state == "in-use":
            volume_id = volume.id
            volumes.append(volume_id)

    return volumes


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
            print(nice_format_message(all_unused_all_regions))
        else:
            print("No available Volumes")
    return all_unused_all_regions


def list_of_profiles():
    all_profiles: list = []
    for profile in boto3.session.Session().available_profiles:
        all_profiles.append(profile)
    return all_profiles


def nice_format_message(unused_ebs_dictionary):
    message = ""
    for region, volumes in unused_ebs_dictionary.items():
        message += "\n"
        for volume in volumes:
            message += f"{volume}\n"
    return message


def format_message(unused_ebs_dict):
    message = f"*Unused EBS Volumes in {selected_profile}*\n"
    for region, volumes in unused_ebs_dict.items():
        message += f"*{region}*\n"
        for volume in volumes:
            message += f"{volume}\n"
    return message


def main():
    message = format_message(describe_unused_ebs_in_all_regions())
    print(message)


if __name__ == "__main__":
    selected_profile = get_user_input(boto3.session.Session().available_profiles)
    session = boto3.setup_default_session(profile_name=selected_profile)
    # schedule.every().day.at("12:15").do(schedule_time_list_unused_ebs)
main()
