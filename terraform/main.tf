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


# Create a new VPC
resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16"  # Replace with your desired CIDR block for the VPC
  tags = {
    Name = "PPP"  # Replace with a name of your choice
  }
}

# Create a subnet within the VPC
resource "aws_subnet" "my_subnet" {
  vpc_id     = aws_vpc.my_vpc.id
  cidr_block = "10.0.1.0/24"  # Replace with your desired CIDR block for the subnet
  availability_zone = "eu-west-1a"  # Replace with your desired availability zone
  tags = {
      project = "ppp"
    }
}

# Create a security group for AWS Batch instances
resource "aws_security_group" "batch_security_group" {
  name_prefix = "BatchSG-"
  vpc_id      = aws_vpc.my_vpc.id

  # Allow SSH access from your local IP address (adjust the source_cidr_block if needed)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["95.91.209.4/32"]  # Replace with your public IP address
  }

  # Allow outbound traffic to the internet
  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
  tags = {
      project = "ppp"
    }

}


# Output the security group IDs
output "batch_security_group_id" {
  value = aws_security_group.batch_security_group.id
}


module storage {
  source = "./storage"
}

module compute {
  source = "./compute"
  ecr_repository_url = module.storage.ecr_repository_url
  subnet_id = aws_subnet.my_subnet.id
  security_group_id = aws_security_group.batch_security_group.id
}
