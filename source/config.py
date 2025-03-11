"""
This file contains the configuration for the application.
"""

import logging
import os

import boto3
import watchtower

AWS_CLOUD_WATCH_LOG_GROUP = os.getenv("AWS_CLOUD_WATCH_LOG_GROUP")
AWS_CLOUD_WATCH_LOG_STREAM = os.getenv("AWS_CLOUD_WATCH_LOG_STREAM")

s3 = boto3.client("s3", endpoint_url="http://localstack:4566")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(
    watchtower.CloudWatchLogHandler(
        log_group=AWS_CLOUD_WATCH_LOG_GROUP,
        stream_name=AWS_CLOUD_WATCH_LOG_STREAM,
        create_log_group=True,
        create_log_stream=True,
        boto3_session=boto3.Session(),
    )
)
