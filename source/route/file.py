"""
This module contains the routes for file operations.
"""

import logging

import botocore
import config
import decorators
import flask

blueprint = flask.Blueprint("file", __name__, url_prefix="/file")


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
        config.s3.upload_fileobj(file, bucket, file.filename)
        logging.info(
            "%s Uploaded file %s to bucket %s.",
            flask.request.remote_addr,
            file.filename,
            bucket,
        )
    except botocore.exceptions.NoCredentialsError:
        return "The credential for the bucket is not configured.", 500

    return "Uploaded file successfully.", 201


@blueprint.route("/<bucket>/<filename>", methods=["GET"])
@decorators.format_response
def download(bucket, filename):
    """
    Fetches a file from the specified bucket.
    """

    try:
        config.s3.download_file(bucket, filename, filename)
        logging.info(
            "%s Downloaded file %s from bucket %s.",
            flask.request.remote_addr,
            filename,
            bucket,
        )

        return "Downloaded file successfully.", 200
    except Exception as error:
        return str(error), 404


@blueprint.route("/<bucket>/<filename>", methods=["DELETE"])
@decorators.format_response
def delete(bucket, filename):
    """
    Deletes a file from the specified bucket.
    """

    try:
        config.s3.delete_object(Bucket=bucket, Key=filename)
        logging.info(
            "%s Deleted file %s from bucket %s.",
            flask.request.remote_addr,
            filename,
            bucket,
        )

        return "Deleted file successfully.", 200
    except Exception as error:
        return str(error), 404
