import boto3
import logging
import os

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'))
aws_region = 'us-west-2'
ec2 = boto3.client('ec2', region_name=aws_region)
logger = logging.getLogger(__name__)


def boto3_tag_list_to_ansible_dict(tags_list):
    tags_dict = {}
    for tag in tags_list:
        if 'key' in tag and not tag['key'].startswith('aws:'):
            tags_dict[tag['key']] = tag['value']
        elif 'Key' in tag and not tag['Key'].startswith('aws:'):
            tags_dict[tag['Key']] = tag['Value']

    return tags_dict


def ansible_dict_to_boto3_tag_list(tags_dict):
    tags_list = []
    for k, v in tags_dict.items():
        tags_list.append({'Key': k, 'Value': v})

    return tags_list
def tag_all():
    boto3_tag_list_to_ansible_dict()

if __name__ == '__main__':
