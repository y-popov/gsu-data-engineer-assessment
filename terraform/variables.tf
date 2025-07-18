variable "s3_access_key" {
  description = "OpenStack S3 access key"
  type        = string
}

variable "s3_secret_key" {
  description = "OpenStack S3 secret key"
  type        = string
}

variable "s3_endpoint" {
  description = "S3 endpoint URL for OpenStack"
  type        = string
}

variable "bronze_bucket_name" {
  description = "S3 bucket name for bronze data"
  type        = string
}

variable "silver_bucket_name" {
  description = "S3 bucket name for silver data"
  type        = string
}
