"""
This file contains the configuration for the application.
"""

import logging
import os

import boto3
import watchtower

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID")
AWS_CLOUD_WATCH_LOGS_ENDPOINT = os.getenv("AWS_CLOUD_WATCH_LOGS_ENDPOINT")
AWS_CLOUD_WATCH_LOGS_LOG_GROUP = os.getenv("AWS_CLOUD_WATCH_LOGS_LOG_GROUP")
AWS_CLOUD_WATCH_LOGS_LOG_STREAM = os.getenv("AWS_CLOUD_WATCH_LOGS_LOG_STREAM")
AWS_S3_ENDPOINT = os.getenv("AWS_S3_ENDPOINT")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
DEFAULT_REGION = os.getenv("DEFAULT_REGION")

session = boto3.Session(
    region_name=DEFAULT_REGION,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_session_token=AWS_SESSION_TOKEN,
    aws_account_id=AWS_SESSION_TOKEN,
)

s3 = session.client("s3", endpoint_url=AWS_S3_ENDPOINT)
logs = session.client("logs", endpoint_url=AWS_CLOUD_WATCH_LOGS_ENDPOINT)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(
    watchtower.CloudWatchLogHandler(
        log_group=AWS_CLOUD_WATCH_LOGS_LOG_GROUP,
        stream_name=AWS_CLOUD_WATCH_LOGS_LOG_STREAM,
        create_log_group=True,
        create_log_stream=True,
        boto3_client=logs,
    )
)
