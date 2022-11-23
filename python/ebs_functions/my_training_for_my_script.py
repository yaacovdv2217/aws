import boto3


# for profile in boto3.session.Session().available_profiles:
#     print(profile)


def list_of_profiles():
    all_profiles: list = []
    for profile in boto3.session.Session().available_profiles:
        all_profiles.append(profile)
    return all_profiles


print(list_of_profiles())
# boto3.setup_default_session(profile_name='big-data')
# AWS_REGION = "us-west-2"
# ec2_resource = boto3.resource('ec2', region_name=AWS_REGION)
# return profile
