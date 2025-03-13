"""
This module contains the controllers for file operations.
"""

import flask

import source.config
import source.service


def generate_presigned_url(bucket: str, filename: str, content_type: str):
    """
    Generates a presigned URL for the specified file in the specified bucket.

    :param bucket: The bucket containing the file.
    :type bucket: str
    :param filename: The name of the file.
    :type filename: str
    :param content_type: The content type of the file.
    :type content_type: str
    :return: The presigned URL.
    :rtype: str
    """

    url: str = source.service.s3_client.generate_presigned_url(
        ClientMethod="put_object",
        HttpMethod="GET",
        Params={
            "Bucket": bucket,
            "Key": filename,
            "ContentType": content_type,
        },
        ExpiresIn=3600 * 24,
    )
    source.service.logs_logger.info(
        "%s generated presigned URL %s for file %s in bucket %s.",
        flask.request.remote_addr,
        url,
        filename,
        bucket,
    )

    if source.config.Environment.ENVIRONMENT == "development":
        url = url.replace("http://localstack", "http://127.0.0.1", 1)

    return url
