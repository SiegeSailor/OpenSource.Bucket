"""
This module contains the controllers for file operations.
"""

import typing

import boto3
import botocore
import flask


def generate_presigned_url(
    client: boto3.client,
    bucket: str,
    filename: str,
    content_type: str,
    **kwargs,
):
    """
    Generates a presigned URL for the specified file in the specified S3 bucket.

    :param boto3.client client: The S3 client.
    :param str bucket: The bucket containing the file.
    :param str filename: The name of the file.
    :param str content_type: The content type of the file.
    :keyword typing.Optional[logging.Logger] logger: The logger.
    :keyword typing.Optional[int] expires_in: The number of seconds the URL is valid for.
        Default to `86400` (24 hours).
    :return: The presigned URL.
    :rtype: str
    """

    url = client.generate_presigned_url(
        ClientMethod="put_object",
        HttpMethod="GET",
        Params={
            "Bucket": bucket,
            "Key": filename,
            "ContentType": content_type,
        },
        ExpiresIn=kwargs.get("expires_in", 3600 * 24),
    )
    if "logger" in kwargs:
        kwargs.get("logger").info(
            "%s generated presigned URL %s for file %s in bucket %s.",
            flask.request.remote_addr,
            url,
            filename,
            bucket,
        )

    return url.replace("localstack", "127.0.0.1", 1)


def upload_file(
    client: boto3.client,
    file: typing.BinaryIO,
    bucket: str,
    **kwargs,
):
    """
    Uploads a file to the specified S3 bucket.

    :param boto3.client client: The S3 client.
    :param typing.BinaryIO file: The file to upload.
    :param str bucket: The bucket to upload the file to.
    :keyword typing.Optional[logging.Logger] logger: The logger.
    :keyword typing.Optional[int] max_age: The number of seconds the URL is valid for.
        Default to `3600` (1 hour).
    :keyword typing.Optional[int] expires_in: The number of seconds the URL is valid for.
        Default to `86400` (24 hours).
    :return: The URL of the uploaded file.
    :rtype: str
    """

    try:
        client.head_bucket(Bucket=bucket)
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "404":
            client.create_bucket(Bucket=bucket)
            client.put_bucket_cors(
                Bucket=bucket,
                ExpectedBucketOwner=flask.current_app.config["AWS_ACCOUNT_ID"],
                CORSConfiguration={
                    "CORSRules": [
                        {
                            "AllowedHeaders": ["*"],
                            "AllowedMethods": ["GET", "POST", "HEAD", "PUT"],
                            "AllowedOrigins": ["*"],
                            "ExposeHeaders": ["ETag"],
                            "MaxAgeSeconds": kwargs.get("max_age", 3600),
                        }
                    ]
                },
            )
            if "logger" in kwargs:
                kwargs.get("logger").info(
                    "%s created bucket %s.",
                    flask.request.remote_addr,
                    bucket,
                )
        else:
            raise

    client.upload_fileobj(Fileobj=file, Bucket=bucket, Key=file.filename)
    if "logger" in kwargs:
        kwargs.get("logger").info(
            "%s uploaded file %s to bucket %s.",
            flask.request.remote_addr,
            file.filename,
            bucket,
        )

    return generate_presigned_url(
        client=client,
        bucket=bucket,
        filename=file.filename,
        content_type=file.content_type,
        logger=kwargs.get("logger"),
        expires_in=kwargs.get("expires_in"),
    )


def delete_file(
    client: boto3.client,
    bucket: str,
    filename: str,
    **kwargs,
):
    """
    Deletes a file from the specified S3 bucket.

    :param boto3.client client: The S3 client.
    :param str bucket: The bucket containing the file.
    :param str filename: The name of the file.
    :keyword typing.Optional[logging.Logger] logger: The logger.
    """

    client.delete_object(Bucket=bucket, Key=filename)
    if "logger" in kwargs:
        kwargs.get("logger").info(
            "%s deleted file %s from bucket %s.",
            flask.request.remote_addr,
            filename,
            bucket,
        )
