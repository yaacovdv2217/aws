import boto3
from pprint import pprint
for profile in boto3.session.Session().available_profiles:
    print(profile)

account_name = boto3.setup_default_session(profile_name='devops-labs')

ec2client = boto3.client('ec2', 'us-west-2')
response = ec2client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
pprint(response)
                                                [{'Name': 'instance-tags-name', 'Values': [""]}]