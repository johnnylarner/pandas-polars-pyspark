TF_STORAGE_MODULE="./../terraform"
JOB_NAME="ppp-test-job"
JOB_QUEUE_NAME=$(terraform -chdir=$TF_STORAGE_MODULE output -raw job_queue_name)
JOB_DEFINITION_NAME=$(terraform -chdir=$TF_STORAGE_MODULE output -raw job_definition_name)


json_response=$(aws batch submit-job \
    --job-name $JOB_NAME \
    --job-queue $JOB_QUEUE_NAME \
    --job-definition $JOB_DEFINITION_NAME \
    --no-cli-pager)

echo "Following submission made:\n$json_response"


job_id=$(python -c "import sys, json; print(json.load(sys.stdin)['jobId'])" <<< $json_response)

job_status="SUBMITTED"
while [[ $job_status != "FAILED" && $job_status != "SUCCEEDED" ]]; do
    echo "Job status: $job_status"
    sleep 5
    job_status=$(aws batch describe-jobs --jobs $job_id --query 'jobs[0].status' --output text --no-cli-pager)
done

echo final job status: $job_status
