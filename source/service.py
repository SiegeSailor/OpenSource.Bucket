"""
This module contains the service configuration and initialization logic.
"""

import logging

import boto3
import config
import watchtower

aws_session = boto3.Session(
    region_name=config.Environment.AWS_DEFAULT_REGION,
    aws_secret_access_key=config.Environment.AWS_SECRET_ACCESS_KEY,
    aws_access_key_id=config.Environment.AWS_ACCESS_KEY_ID,
    aws_session_token=config.Environment.AWS_SESSION_TOKEN,
    aws_account_id=config.Environment.AWS_SESSION_TOKEN,
)

s3_client = aws_session.client("s3", endpoint_url=config.Environment.AWS_S3_ENDPOINT)
logs_client = aws_session.client(
    "logs", endpoint_url=config.Environment.AWS_CLOUDWATCH_LOGS_ENDPOINT
)

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        watchtower.CloudWatchLogHandler(
            log_group=config.Environment.AWS_CLOUDWATCH_LOGS_LOG_GROUP,
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
        log_group=config.Environment.AWS_CLOUDWATCH_LOGS_LOG_GROUP,
        stream_name="service",
        create_log_group=True,
        create_log_stream=True,
        boto3_client=logs_client,
    )
)
