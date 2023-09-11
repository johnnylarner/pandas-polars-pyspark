TF_STORAGE_MODULE="./../terraform"
BUCKET_NAME=$(terraform -chdir=$TF_STORAGE_MODULE output -raw bucket_name)

echo "BUCKET_NAME: $BUCKET_NAME"

aws s3 sync ../data s3://$BUCKET_NAME/data
