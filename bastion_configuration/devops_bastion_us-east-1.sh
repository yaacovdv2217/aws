#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <bastion-name> <instance-name>"
    exit 1
fi

INSTANCE_NAME="$1"

# Debug output
echo "INSTANCE_NAME: $INSTANCE_NAME"


# Set the AWS profile
AWS_PROFILE="devops-labs"

# SSH forwarding (use a different local port if 2222 is in use)
# LOCAL_PORT=22

# SSH to the Bastion server with agent forwarding
# ssh -A -i "$BASTION_KEY" -L "$LOCAL_PORT":localhost:22 -N -p 22 "$BASTION_USER@$BASTION_IP"
#
# # Now you can SSH to the private instance
# ssh -i "$BASTION_KEY" -p "$LOCAL_PORT" ec2-user@private_instance_ip

# Run the AWS CLI command to describe the specified instance
INSTANCE_IP=$(aws ec2 \
  --region us-east-1 \
  describe-instances \
  --profile "$AWS_PROFILE" \
  --query "Reservations[].Instances[?Tags[?Key == 'Name' && contains(Value, '"${INSTANCE_NAME}"')][]][]" | jq -r '.[] | "\(.PrivateIpAddress) - \(.Tags[] | select(.Key == "Name").Value)"' | fzf)

echo "Instance ${INSTANCE_IP}"
INSTANCE_IP_CLEAN=$(awk -F- '{print $1}' <<<"$INSTANCE_IP")
BASTION_IP="44.214.141.204"
BASTION_USER="ec2-user"
BASTION_KEY="/Users/yaacov/desktop/pems/key_pems_aws/aws_n.virginia/DevSecOps_keeper.pem"
ssh -J ${BASTION_USER}@${BASTION_IP} -i ${BASTION_KEY} ec2-user@${INSTANCE_IP_CLEAN}