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
