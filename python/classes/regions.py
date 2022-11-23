import boto3

account_name = boto3.setup_default_session(profile_name='big-data')
ec2_resource = boto3.resource('ec2', region_name='us-east-1')
global_regions_dict: dict = {}
service: str = 'ec2'


def available_regions():
    regions: list = []
    client = boto3.client(service)
    dict_of_regions = client.describe_regions()
    for item in dict_of_regions["Regions"]:
        regions.append(item["RegionName"])
        global_regions_dict[item["RegionName"]] = []
    return regions


print(available_regions())

# account_name = boto3.setup_default_session(profile_name='big-data')
# ec2c = boto3.client('ec2')
# print(ec2c.describe_regions())
