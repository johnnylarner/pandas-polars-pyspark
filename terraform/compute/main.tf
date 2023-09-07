data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "compute_assume_ecs_instance_role" {
  name               = "ecs_instance_role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}

resource "aws_iam_role_policy_attachment" "compute_assume_ecs_instance_role" {
  role       = aws_iam_role.compute_assume_ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_instance_profile" "compute_ecs_instance_role" {
  name = "ecs_instance_role"
  role = aws_iam_role.compute_assume_ecs_instance_role.name
}

data "aws_iam_policy_document" "batch_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["batch.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "compute_batch_service_role" {
  name               = "aws_batch_service_role"
  assume_role_policy = data.aws_iam_policy_document.batch_assume_role.json
}

resource "aws_iam_role_policy_attachment" "compute_batch_service_role" {
  role       = aws_iam_role.compute_batch_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}



resource "aws_batch_compute_environment" "ppp_compute_environment" {
  compute_environment_name = "ppp_compute_environment"

  compute_resources {
    instance_role = aws_iam_instance_profile.compute_ecs_instance_role.arn

    instance_type = [
      "optimal",
      "m5.large"
    ]

    max_vcpus = 16
    min_vcpus = 0

    security_group_ids = var.security_group_ids
    subnets = var.subnet_ids
    type = "EC2"
  }

  service_role = aws_iam_role.compute_batch_service_role.arn
  type         = "MANAGED"
  depends_on   = [aws_iam_role_policy_attachment.compute_batch_service_role]

  lifecycle {
    create_before_destroy = true
  }
}

# Create an AWS Batch job queue
resource "aws_batch_job_queue" "ppp_job_queue" {
  name = "ppp_job_queue"
  state = "ENABLED"
  priority = 1
  compute_environments = [aws_batch_compute_environment.ppp_compute_environment.arn]
}

resource "aws_batch_job_definition" "ppp_job_definition" {
  name = "ppp_job_definition"  # Replace with your desired job definition name
  type = "container"

  container_properties = jsonencode({
    image = "public.ecr.aws/amazonlinux/amazonlinux:latest"
    command = ["echo", "hello world"]
      resourceRequirements = [
      {
        type  = "VCPU"
        value = "1"
      },
      {
        type  = "MEMORY"
        value = "256"
      }
    ]
  })
}

output "job_queue_name" {
  value = aws_batch_job_queue.ppp_job_queue.name
}

output "job_definition_name" {
  value = aws_batch_job_definition.ppp_job_definition.name
}
