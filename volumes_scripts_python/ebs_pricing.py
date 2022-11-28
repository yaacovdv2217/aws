import boto3
from datetime import datetime

GLOBAL_REGIONS_DICT: dict = {}
CURRENT_DATE = datetime.today().strftime("%Y-%m-%d")
TIME_CURRENT_DATE = datetime.strptime(CURRENT_DATE, "%Y-%m-%d")
ebs_name_map = {
    'gp3': 0.08,
    'gp2': 0.1,
    'io2': 0.125,
    'sc1': 0.015
}


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


def describe_unused_ebs(region):
    regional_client = boto3.resource("ec2", region_name=region)
    volumes = []
    for volume in regional_client.volumes.filter(
            Filters=[{"Name": "status", "Values": ["gp2", "gp3", "io2", "sc1"]}]
    ):
        if volume.volumetype == "gp2":
            volume_volumetype = volume.volumetype
            volumes.append(volume_volumetype)

    return volumes
