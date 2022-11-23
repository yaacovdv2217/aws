import boto3
for profile in boto3.session.Session().available_profiles:
    print(profile)

boto3.setup_default_session(profile_name='big-data')
AWS_REGION = "us-west-2"
ec2_resource = boto3.resource('ec2', region_name=AWS_REGION)


def unused_ebs_in_specific_region():
    all_volumes = []
    for volume in ec2_resource.volumes.filter(
            Filters=[{'Name': 'status', 'Values': ['available']}]):

        if volume.state == "available":
            volume_id = volume.id
            all_volumes.append({volume_id, volume.state})
    return all_volumes


def format_message(unused_ebs_dict):
    message = f"*Unused EBS Volumes in *\n"
    for region, volumes in unused_ebs_dict.items():
        message += f"*{region}*\n"
        for volume in volumes:
            message += f"{volume}\n"
    return message


message = format_message(unused_ebs_in_specific_region())
print(message)
