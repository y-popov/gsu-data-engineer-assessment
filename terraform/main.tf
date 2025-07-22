terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket                      = "ip13-tf-states"
    key                         = "terraform.tfstate"
    region                      = "us-east-1"
    skip_s3_checksum            = true
    skip_credentials_validation = true
    skip_requesting_account_id  = true
    use_path_style              = false
    # Note: access_key, secret_key, and endpoint will be provided through environment variables
  }
}

provider "aws" {
  region                      = "us-east-1"
  s3_use_path_style           = false
  skip_requesting_account_id  = true
  skip_credentials_validation = true
}

resource "aws_s3_bucket" "bronze" {
  bucket = var.bronze_bucket
}

resource "aws_s3_bucket" "silver" {
  bucket = var.silver_bucket
}
