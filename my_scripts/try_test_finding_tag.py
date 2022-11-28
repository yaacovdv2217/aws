import boto3
PROFILE_NAME = 'devops-labs'
boto3.setup_default_session(profile_name=PROFILE_NAME)
aws_region = 'us-west-2'
regional_client = boto3.resource("ec2", region_name=aws_region)
volumes = []
# for volume in regional_client.volumes.filter(
#         Filters=[
#             {
#                 'Name': 'status',
#                 'Values': [
#                     'available',
#                 ]
#             }
#
#         ]
# ):
#     volume_id = volume.id
#     volumes.append(volume_id)
#
# tagged_volumes = []
# for volume in regional_client.volumes.filter(Filters=[{'Name': 'tag:Name', 'Values': ['stateful']}]):
#     volumes.append(volume)
#     # print(tagged_volumes)
#
#     # tagged_volumes = [volumes for volumes in volumes if volumes not in tagged_volumes]
#     # for volume in tagged_volumes:
#     print(volume)


response = regional_client.create_volume(
    AvailabilityZone=aws_region,
    Size=20,
    VolumeType='gp2',
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'yaacov_test3'
                },
            ]
        },
    ],
)
