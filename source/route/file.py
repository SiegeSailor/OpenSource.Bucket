"""
This module contains the routes for file operations.
"""

import botocore
import flask

import source.client
import source.config
import source.controller
import source.decorator

blueprint = flask.Blueprint("file", __name__, url_prefix="/file")


@blueprint.route("/<bucket>", methods=["POST"])
@source.decorator.format_response
def upload_file(bucket: str):
    """
    Uploads a file to the specified bucket.
    """

    try:
        file = flask.request.files["file"]
    except KeyError:
        return "File is not provided.", 400

    try:
        source.client.s3_client.head_bucket(Bucket=bucket)
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "404":
            source.client.s3_client.create_bucket(Bucket=bucket)
            source.client.s3_client.put_bucket_cors(
                Bucket=bucket,
                ExpectedBucketOwner=source.config.Environment.AWS_ACCOUNT_ID,
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
            source.client.logs_logger.info(
                "%s created bucket %s.",
                flask.request.remote_addr,
                bucket,
            )
        else:
            raise

    source.client.s3_client.upload_fileobj(
        Fileobj=file, Bucket=bucket, Key=file.filename
    )
    source.client.logs_logger.info(
        "%s uploaded file %s to bucket %s.",
        flask.request.remote_addr,
        file.filename,
        bucket,
    )

    url = source.controller.file.generate_presigned_url(
        bucket=bucket, filename=file.filename, content_type=file.content_type
    )

    return "Uploaded file successfully.", 201, {"location": url}


@blueprint.route("/<bucket>/<filename>", methods=["GET"])
@source.decorator.format_response
def generate_url(bucket, filename):
    """
    Fetches a file from the specified bucket.
    """

    metadata = source.client.s3_client.head_object(Bucket=bucket, Key=filename)

    url = source.controller.file.generate_presigned_url(
        bucket=bucket, filename=filename, content_type=metadata["ContentType"]
    )

    return "Generated file URL successfully.", 200, {"location": url}


@blueprint.route("/<bucket>/<filename>", methods=["DELETE"])
@source.decorator.format_response
def delete(bucket, filename):
    """
    Deletes a file from the specified bucket.
    """

    source.client.s3_client.delete_object(Bucket=bucket, Key=filename)
    source.client.logs_logger.info(
        "%s deleted file %s from bucket %s.",
        flask.request.remote_addr,
        filename,
        bucket,
    )

    return "Deleted file successfully.", 200
