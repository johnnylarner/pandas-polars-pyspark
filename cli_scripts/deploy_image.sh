#!/bin/bash
REPO_ROOT="./.."
IMAGE_NAME_AND_TAG="ppp-dev:dev"
IMAGE_TAG="dev"


# Add debug output for terraform directory
TF_STORAGE_MODULE=$REPO_ROOT/terraform
echo "TF_STORAGE_MODULE: $TF_STORAGE_MODULE"

# Extract outputs from current terraform state
ECR_REPO_URL=$(terraform -chdir=$TF_STORAGE_MODULE output -raw ecr_repository_url)
ECR_URL=$( echo $ECR_REPO_URL | cut -d/ -f1)
AWS_REGION=$(terraform -chdir=$TF_STORAGE_MODULE output -raw aws_region)

# Add debug output for extracted variables
echo "ECR_REPO_URL: $ECR_REPO_URL"
echo "ECR_URL: $ECR_URL"
echo "AWS_REGION: $AWS_REGION"

# Extract credentials for docker login
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_USER_NAME=$(aws sts get-caller-identity \
    --query Arn --output text | cut -d/ -f2)

# Login, build and push
aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin $ECR_URL

docker buildx build --platform=linux/amd64  -t $IMAGE_NAME_AND_TAG $REPO_ROOT
docker image tag $IMAGE_NAME_AND_TAG $ECR_REPO_URL:$IMAGE_TAG
docker push $ECR_REPO_URL:$IMAGE_TAG
