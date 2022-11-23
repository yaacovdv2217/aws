import boto3

aws_region = 'us-west-2'
boto3.setup_default_session(profile_name='devops-labs')
client = boto3.resource('ec2', region_name=aws_region)

new_volume = client.create_volume(
    AvailabilityZone=f"{aws_region}",
    Size=10,
    VolumeType='gp2',
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [{'Key': 'yaacov', 'Value': 'yaacov_test3'}]}])

print(f'Created Volume ID: {new_volume["VolumeId"]}')
