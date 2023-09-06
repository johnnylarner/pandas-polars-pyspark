terraform {
  backend "s3" {
    bucket = "pandas-polars-pyspark-terraform-state"
    key    = "default"
    region = "eu-west-1"
  }
}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [aws_default_vpc.default.id]
  }
}


resource "aws_default_security_group" "default" {
  vpc_id = aws_default_vpc.default.id

  ingress {
    protocol  = -1
    self      = true
    from_port = 0
    to_port   = 0
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


module "storage" {
  source = "./storage"
}

module "compute" {
  source             = "./compute"
  ecr_repository_url = module.storage.ecr_repository_url
  subnet_ids         = data.aws_subnets.default.ids
  security_group_ids = [aws_default_security_group.default.id]
}
