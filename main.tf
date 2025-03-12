provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name

  lifecycle_rule {
    id      = "log"
    enabled = true

    transition {
      days          = 30
      storage_class = var.storage_class
    }

    expiration {
      days = 365
    }
  }
}

variable "bucket_name" {
  description = "The name of the S3 bucket"
}

variable "storage_class" {
  description = "The storage class for S3"
  default     = "STANDARD"
}