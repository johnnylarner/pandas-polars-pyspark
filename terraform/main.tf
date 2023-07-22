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

resource "aws_vpc" "default" {
}


module storage {
  source = "./storage"
}

module compute {
  source = "./compute"
  vpc_id = aws_vpc.default.id
}
