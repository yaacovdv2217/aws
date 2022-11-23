import boto3

for profile in boto3.session.Session().available_profiles:
    print(profile)

account_name = boto3.setup_default_session(profile_name='big-data')
# access_key = "XXXXXXXXXXXXXXXXXX"
# secret_key = "XXXXXXXXXXXXXXXXXX"

# for i, k in enumerate(""):
# print("{} ) {}".format(str(i + 1), k))

client = boto3.client('ec2', region_name='us-east-1')

ec2_regions = [region['RegionName']
               for region in client.describe_regions()['Regions']]


for region in ec2_regions:

    conn = boto3.resource('ec2', region_name=region)
    instances = conn.instances.filter()
    for instance in instances:
        if instance.state["Name"] == "terminated":
            print(instance.id, instance.instance_type, region)
