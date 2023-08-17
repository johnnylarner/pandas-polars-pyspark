# IAM Role for batch processing
resource "aws_iam_role" "batch_role" {
  name               = "batch_role"
  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement":
    [
      {
          "Action": "sts:AssumeRole",
          "Effect": "Allow",
          "Principal": {
            "Service": "batch.amazonaws.com"
          }
      }
    ]
}
EOF
tags = {
    project = "ppp"
  }
}
# Attach the Batch policy to the Batch role
resource "aws_iam_role_policy_attachment" "policy_attachment" {
  role       = aws_iam_role.batch_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}

resource "aws_iam_instance_profile" "batch_instance_profile" {
  name = "BatchInstanceProfile"  # Replace with your desired instance profile name

  role = aws_iam_role.batch_role.id  # Replace with the ID of the IAM role you want to associate
}



# Extract the IAM role ARN
output "batch_role_arn" {
  value = aws_iam_role.batch_role.arn
}


# Define the AWS Batch job definition
resource "aws_batch_job_definition" "my_job_definition" {
  name = "my-batch-job"  # Replace with your desired job definition name
  type = "container"

  container_properties = jsonencode({
    image = var.ecr_repository_url
      resourceRequirements = [
      {
        type  = "VCPU"
        value = "4"
      },
      {
        type  = "MEMORY"
        value = "8192"
      }
    ]
  })
}

# Create an AWS Batch compute environment
resource "aws_batch_compute_environment" "my_compute_environment" {
  service_role = aws_iam_role.batch_role.arn  # Replace with the actual Batch service role ARN
  compute_environment_name = "my-compute-env"  # Replace with your desired compute environment name
  type = "MANAGED"

  compute_resources {
    type = "EC2"
    instance_role = aws_iam_instance_profile.batch_instance_profile.arn  # Replace with the actual instance role ARN
    instance_type = ["m5.large"]
    min_vcpus = 0
    max_vcpus = 4
    subnets = [var.subnet_id]
    security_group_ids = [var.security_group_id]
  }
}

# # Create an AWS Batch job queue
# resource "aws_batch_job_queue" "my_job_queue" {
#   name = "my-job-queue"  # Replace with your desired job queue name
#   priority = 1
#   compute_environment_order {
#     order = 1
#     compute_environment = aws_batch_compute_environment.my_compute_environment.arn
#   }
# }

# # Create an AWS Batch job
# resource "aws_batch_job" "my_batch_job" {
#   name = "my-batch-job-run"  # Replace with your desired job name
#   job_queue = aws_batch_job_queue.my_job_queue.arn
#   job_definition = aws_batch_job_definition.my_job_definition.arn
# }
