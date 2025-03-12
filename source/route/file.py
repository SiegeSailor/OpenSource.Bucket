"""
This module contains the routes for file operations.
"""

import botocore
import config
import decorators
import flask

blueprint = flask.Blueprint("file", __name__, url_prefix="/file")
# 1. Set newly created bucket CORS
# 2. Presigned URL for file upload
# 3. Presigned POST for file upload


@blueprint.route("/<bucket>", methods=["POST"])
@decorators.format_response
def upload(bucket: str):
    """
    Uploads a file to the specified bucket.
    """

    try:
        file = flask.request.files["file"]
    except KeyError:
        return "File is not provided.", 400

    try:
        config.s3_client.head_bucket(Bucket=bucket)
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "404":
            config.s3_client.create_bucket(Bucket=bucket)
            config.s3_client.put_bucket_cors(
                Bucket=bucket,
                ExpectedBucketOwner=config.AWS_ACCOUNT_ID,
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
            config.logs_logger.info(
                "%s created bucket %s.",
                flask.request.remote_addr,
                bucket,
            )
        else:
            raise

    config.s3_client.upload_fileobj(file, bucket, file.filename)
    config.logs_logger.info(
        "%s uploaded file %s to bucket %s.",
        flask.request.remote_addr,
        file.filename,
        bucket,
    )

    url = config.s3_client.generate_presigned_url(
        ClientMethod="put_object",
        HttpMethod="GET",
        Params={
            "Bucket": bucket,
            "Key": file.filename,
            "ContentType": file.content_type,
        },
        ExpiresIn=3600 * 24,
    )
    config.logs_logger.info(
        "%s generated presigned URL %s for file %s in bucket %s.",
        flask.request.remote_addr,
        url,
        file.filename,
        bucket,
    )

    if config.ENVIRONMENT == "development":
        url = url.replace("http://localstack", "http://127.0.0.1")

    return "Uploaded file successfully.", 201, {"location": url}


@blueprint.route("/<bucket>/<filename>", methods=["GET"])
@decorators.format_response
def download(bucket, filename):
    """
    Fetches a file from the specified bucket.
    """

    path_file = f"/{bucket}/{filename}"
    try:
        config.s3_client.download_file(bucket, filename, path_file)
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "404":
            return f"File {filename} not found in {bucket}.", 404

        raise
    config.logs_logger.info(
        "%s downloaded file %s from bucket %s.",
        flask.request.remote_addr,
        filename,
        bucket,
    )

    return flask.send_file(path_file, as_attachment=True), 200


@blueprint.route("/<bucket>/<filename>", methods=["DELETE"])
@decorators.format_response
def delete(bucket, filename):
    """
    Deletes a file from the specified bucket.
    """

    config.s3_client.delete_object(Bucket=bucket, Key=filename)
    config.logs_logger.info(
        "%s deleted file %s from bucket %s.",
        flask.request.remote_addr,
        filename,
        bucket,
    )

    return "Deleted file successfully.", 200
