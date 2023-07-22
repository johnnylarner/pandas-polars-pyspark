resource "aws_s3_bucket" "my_bucket" {
  bucket = "pandas-polars-pyspark"
  acl    = "private"

  tags = {
    project        = "ppp"
  }
}

resource "aws_ecr_repository" "my_repository" {
  name = "pandas-polars-pyspark"
}
