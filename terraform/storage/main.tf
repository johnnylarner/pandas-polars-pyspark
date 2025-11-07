resource "aws_s3_bucket" "my_bucket" {
  bucket = "pandas-polars-pyspark"
  acl    = "private"

  tags = {
    project        = "ppp"
  }
}

resource "aws_ecr_repository" "my_repository" {
  name = "pandas-polars-pyspark"
    image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }

  # Other attributes specific to your ECR repository configuration

  lifecycle {
    ignore_changes = [
      # Exclude changes to the image_tag_mutability attribute
      "image_tag_mutability",
      # Exclude changes to the image_scanning_configuration attribute
      "image_scanning_configuration",
      # Add more attributes if needed
    ]
  }
}

output "ecr_repository_url" {
  value = aws_ecr_repository.my_repository.repository_url
}
