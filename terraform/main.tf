terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region  = "us-east-1"
  access_key = var.s3_access_key
  secret_key = var.s3_secret_key

  endpoints {
    s3 = var.s3_endpoint
  }

  s3_use_path_style = false
  skip_requesting_account_id = true
  skip_credentials_validation = true
}

resource "aws_s3_bucket" "bronze" {
  bucket   = var.bronze_bucket_name
}

resource "aws_s3_bucket" "silver" {
  bucket   = var.silver_bucket_name
}
