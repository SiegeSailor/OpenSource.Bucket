"""
This module contains the routes for file operations.
"""

import botocore
import config
import controller
import decorators
import flask
import service

blueprint = flask.Blueprint("file", __name__, url_prefix="/file")


@blueprint.route("/<bucket>", methods=["POST"])
@decorators.format_response
def upload_file(bucket: str):
    """
    Uploads a file to the specified bucket.
    """

    try:
        file = flask.request.files["file"]
    except KeyError:
        return "File is not provided.", 400

    try:
        service.s3_client.head_bucket(Bucket=bucket)
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "404":
            service.s3_client.create_bucket(Bucket=bucket)
            service.s3_client.put_bucket_cors(
                Bucket=bucket,
                ExpectedBucketOwner=config.Environment.AWS_ACCOUNT_ID,
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
            service.logs_logger.info(
                "%s created bucket %s.",
                flask.request.remote_addr,
                bucket,
            )
        else:
            raise

    service.s3_client.upload_fileobj(Fileobj=file, Bucket=bucket, Key=file.filename)
    service.logs_logger.info(
        "%s uploaded file %s to bucket %s.",
        flask.request.remote_addr,
        file.filename,
        bucket,
    )

    url = controller.file.generate_presigned_url(
        bucket=bucket, filename=file.filename, content_type=file.content_type
    )

    return "Uploaded file successfully.", 201, {"location": url}


@blueprint.route("/<bucket>/<filename>", methods=["GET"])
@decorators.format_response
def generate_url(bucket, filename):
    """
    Fetches a file from the specified bucket.
    """

    metadata = service.s3_client.head_object(Bucket=bucket, Key=filename)

    url = controller.file.generate_presigned_url(
        bucket=bucket, filename=filename, content_type=metadata["ContentType"]
    )

    if config.Environment.ENVIRONMENT == "development":
        url = url.replace("http://localstack", "http://127.0.0.1")

    return "Generated file URL successfully.", 200, {"location": url}


@blueprint.route("/<bucket>/<filename>", methods=["DELETE"])
@decorators.format_response
def delete(bucket, filename):
    """
    Deletes a file from the specified bucket.
    """

    service.s3_client.delete_object(Bucket=bucket, Key=filename)
    service.logs_logger.info(
        "%s deleted file %s from bucket %s.",
        flask.request.remote_addr,
        filename,
        bucket,
    )

    return "Deleted file successfully.", 200
