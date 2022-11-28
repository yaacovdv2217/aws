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


PROFILE_NAME = 'devops-labs'
boto3.setup_default_session(profile_name=PROFILE_NAME)
aws_region = "us-west-2"
ec2 = boto3.resource('ec2', aws_region)
snapshot = ec2.Snapshot('id')

Region = 'us-west-2'
for vol in ec2.volumes.all():
    if Region == 'us-west-2':
        string = vol.id
        ec2.create_snapshot(VolumeId=vol.id, Description=string)
        print(vol.id),
        print(f"A snapshot{snapshot} has been created for the following EBS volumes', vol.id")
    else:
        print(f"No snapshot has been created for the following EBS volumes', {vol.id}")
