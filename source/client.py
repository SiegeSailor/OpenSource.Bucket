"""
This module contains the service configuration and initialization logic.
"""

import logging
import typing

import boto3
import watchtower


class AWS:
    """
    This class is an AWS client factory.

    :keyword typing.Optional[str] region: The region of AWS.
    :keyword typing.Optional[str] secret_access_key: The secret access key of AWS. It is
        available on [AWS Account Overview](https://console.aws.amazon.com/).
    :keyword typing.Optional[str] access_key_id: The access key id of AWS. It is available
        on [AWS Account Overview](https://console.aws.amazon.com/).
    :keyword typing.Optional[str] session_token: The session token of AWS. It is available
        with [AWS STS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html).
    :keyword typing.Optional[str] account_id: A 12-digit number. It is available on
        [AWS Account Overview](https://console.aws.amazon.com/).
    """

    def __init__(self, **kwargs):
        self._session = boto3.Session(
            region_name=kwargs.get("region"),
            aws_secret_access_key=kwargs.get("secret_access_key"),
            aws_access_key_id=kwargs.get("access_key_id"),
            aws_session_token=kwargs.get("session_token"),
            aws_account_id=kwargs.get("account_id"),
        )

    def create_client(self, service: str, **kwargs):
        """
        Create a service client.

        :param str service: The service name.
        :keyword typing.Optional[str] endpoint_url: The endpoint URL of the S3 client.
        :return: The service client.
        :rtype: boto3.client
        """

        return self._session.client(service, endpoint_url=kwargs.get("endpoint_url"))

    def create_logger(
        self,
        group: str,
        stream: str,
        client: boto3.client,
        name: typing.Optional[str],
    ):
        """
        Create a logger for CloudWatch Logs.

        :param str name: The name of the logger.
        :param str group: The name of the log group.
        :param boto3.client client: The CloudWatch Logs client.
        :return: The logger.
        :rtype: logging.Logger
        """

        logs_logger = logging.getLogger(name)
        logs_logger.setLevel(logging.INFO)
        logs_logger.addHandler(logging.StreamHandler())
        logs_logger.addHandler(
            watchtower.CloudWatchLogHandler(
                log_group_name=group,
                log_stream_name=stream,
                create_log_group=True,
                create_log_stream=True,
                boto3_client=client,
            )
        )

        return logs_logger
