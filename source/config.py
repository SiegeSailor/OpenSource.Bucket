"""
This file contains the configuration for the application.
"""

import logging
import os

import boto3
import watchtower

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID")
AWS_CLOUDWATCH_LOGS_ENDPOINT = os.getenv("AWS_CLOUDWATCH_LOGS_ENDPOINT")
AWS_CLOUDWATCH_LOGS_LOG_GROUP = os.getenv("AWS_CLOUDWATCH_LOGS_LOG_GROUP")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_S3_ENDPOINT = os.getenv("AWS_S3_ENDPOINT")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
ENVIRONMENT = os.getenv("ENVIRONMENT")

aws_session = boto3.Session(
    region_name=AWS_DEFAULT_REGION,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_session_token=AWS_SESSION_TOKEN,
    aws_account_id=AWS_SESSION_TOKEN,
)

s3_client = aws_session.client("s3", endpoint_url=AWS_S3_ENDPOINT)
logs_client = aws_session.client("logs", endpoint_url=AWS_CLOUDWATCH_LOGS_ENDPOINT)

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        watchtower.CloudWatchLogHandler(
            log_group=AWS_CLOUDWATCH_LOGS_LOG_GROUP,
            stream_name="default",
            create_log_group=True,
            create_log_stream=True,
            boto3_client=logs_client,
        ),
    ],
)
logs_logger = logging.getLogger(__name__)
logs_logger.setLevel(logging.INFO)
logs_logger.addHandler(logging.StreamHandler())
logs_logger.addHandler(
    watchtower.CloudWatchLogHandler(
        log_group=AWS_CLOUDWATCH_LOGS_LOG_GROUP,
        stream_name="service",
        create_log_group=True,
        create_log_stream=True,
        boto3_client=logs_client,
    )
)
