"""
This file contains the configuration for the application.
"""

import boto3

s3 = boto3.client("s3", endpoint_url="http://localstack:4566")
