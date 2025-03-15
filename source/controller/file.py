"""
This module contains the controllers for file operations.
"""

import logging
import typing

import boto3
import botocore
import flask


def generate_presigned_url(
    s3_client: boto3.client,
    logger: logging.Logger,
    bucket: str,
    filename: str,
    content_type: str,
    is_replacing: bool = False,
):
    """
    Generates a presigned URL for the specified file in the specified S3 bucket.

    :param str bucket: The bucket containing the file.
    :param str filename: The name of the file.
    :param str content_type: The content type of the file.
    :param bool is_replacing: Whether the `localstack` string is replaced with `127.0.0.1`.
    :return: The presigned URL.
    :rtype: str
    """

    print("=========")

    url: str = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        HttpMethod="GET",
        Params={
            "Bucket": bucket,
            "Key": filename,
            "ContentType": content_type,
        },
        ExpiresIn=3600 * 24,
    )
    logger.info(
        "%s generated presigned URL %s for file %s in bucket %s.",
        flask.request.remote_addr,
        url,
        filename,
        bucket,
    )
    print(url)
    if is_replacing:
        url = url.replace("localstack", "127.0.0.1", 1)

    return url


def upload_file(
    s3_client: boto3.client,
    logger: logging.Logger,
    file: typing.BinaryIO,
    bucket: str,
    is_replacing: bool = False,
):
    """
    Uploads a file to the specified S3 bucket.

    :param boto3.client s3_client: The S3 client.
    :param logging.Logger logger: The logger.
    :param typing.BinaryIO file: The file to upload.
    :param str bucket: The bucket to upload the file to.
    :return: The URL of the uploaded file.
    :rtype: str
    """

    try:
        s3_client.head_bucket(Bucket=bucket)
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "404":
            s3_client.create_bucket(Bucket=bucket)
            s3_client.put_bucket_cors(
                Bucket=bucket,
                ExpectedBucketOwner=flask.current_app.config["AWS_ACCOUNT_ID"],
                CORSConfiguration={
                    "CORSRules": [
                        {
                            "AllowedHeaders": ["*"],
                            "AllowedMethods": ["GET", "POST", "HEAD", "PUT"],
                            "AllowedOrigins": ["*"],
                            "ExposeHeaders": ["ETag"],
                            "MaxAgeSeconds": 3600,
                        }
                    ]
                },
            )
            logger.info(
                "%s created bucket %s.",
                flask.request.remote_addr,
                bucket,
            )
        else:
            raise

    s3_client.upload_fileobj(Fileobj=file, Bucket=bucket, Key=file.filename)
    logger.info(
        "%s uploaded file %s to bucket %s.",
        flask.request.remote_addr,
        file.filename,
        bucket,
    )

    url = generate_presigned_url(
        s3_client=s3_client,
        logger=logger,
        bucket=bucket,
        filename=file.filename,
        content_type=file.content_type,
        is_replacing=is_replacing,
    )

    return url


def delete_file(
    s3_client: boto3.client,
    logger: logging.Logger,
    bucket: str,
    filename: str,
):
    """
    Deletes a file from the specified S3 bucket.

    :param boto3.client s3_client: The S3 client.
    :param logging.Logger logger: The logger.
    :param str bucket: The bucket containing the file.
    :param filename: The name of the file.
    :type filename: str
    """

    s3_client.delete_object(Bucket=bucket, Key=filename)
    logger.info(
        "%s deleted file %s from bucket %s.",
        flask.request.remote_addr,
        filename,
        bucket,
    )
