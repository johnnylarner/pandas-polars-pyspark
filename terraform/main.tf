terraform {
  backend "s3" {
    bucket         = "pandas-polars-pyspark-terraform-state"
    key            = "default"
    region         = "eu-west-1"
  }
}

provider "aws" {
  region = "eu-west-1"
}


data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids"  "all_default_subnets" {
  vpc_id =  data.aws_vpc.default.subnet_ids
  }

module storage {
  source = "./storage"
}

module compute {
  source = "./compute"
}
