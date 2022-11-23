import boto3

for profile in boto3.session.Session().available_profiles:
    print(profile)

account_name = boto3.setup_default_session(profile_name='big-data')

AWS_REGION = "us-west-2"

ec2_resource = boto3.resource('ec2', region_name=AWS_REGION)

for volume in ec2_resource.volumes.filter(
    VolumeIds=[
        'vol-0eb2b9a495cfd809e',
        'vol-0e0d40104bc4e0e60',
    ],
):
    print(f'Volume {volume.id} ({volume.size} GiB) -> {volume.state}')

