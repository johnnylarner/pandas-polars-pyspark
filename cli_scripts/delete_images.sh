#!/bin/bash
REPO_ROOT="./.."
DOCKER_IMAGE_NAME="ppp-dev"
DOCKER_IMAGE_NAME_TAG="latest"

# Add debug output for terraform directory
TF_STORAGE_MODULE=$REPO_ROOT/terraform
echo "TF_STORAGE_MODULE: $TF_STORAGE_MODULE"

# Extract outputs from current terraform state
ECR_REPO_URL=$(terraform -chdir=$TF_STORAGE_MODULE output -raw ecr_repository_url)
ECR_URL=$( echo $ECR_REPO_URL | cut -d/ -f1)
ECR_REPO_NAME=$( echo $ECR_REPO_URL | cut -d/ -f2)
AWS_REGION=$(terraform -chdir=$TF_STORAGE_MODULE output -raw aws_region)

# Add debug output for extracted variables
echo "ECR_REPO_URL: $ECR_REPO_URL"
echo "ECR_URL: $ECR_URL"
echo "ECR_REPO_NAME: $ECR_REPO_NAME"
echo "AWS_REGION: $AWS_REGION"

# Extract credentials for docker login
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_USER_NAME=$(aws sts get-caller-identity \
    --query Arn --output text | cut -d/ -f2)

# Login, build and push
aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin $ECR_URL


image_ids=$(aws ecr list-images \
    --repository-name $ECR_REPO_NAME --query 'imageIds[*]' --output json)

if [ "$image_ids" != "[]" ]; then
  # Loop through and delete each image
    for image_id in $image_ids; do
        echo "Deleting image: $image_id"
        aws ecr batch-delete-image \
        --repository-name $ECR_REPO_NAME --image-ids "$image_id" --no-cli-pager
    done
fi

echo "All images deleted from ECR repository: $ECR_REPO_NAME"
