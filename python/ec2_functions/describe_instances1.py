import boto3
import sys
from pprint import pprint
import configparser

aws_config = configparser.ConfigParser()
aws_config.read('~/.aws/credentials')

for key in aws_config.sections():
    print(key)
sys.exit(0)
# global variables


client = boto3.client('ec2')

for each_inst in client.describe_instances()['Reservations']:
    for inst_id in each_inst['Instances']:
        pprint(inst_id['InstanceId'])

for acct in accounts:
    session = boto3.Session(profile_name=acct)
    iam = session.client('iam')
    for user in usernames:
        iam.create_user(UserName=user)
