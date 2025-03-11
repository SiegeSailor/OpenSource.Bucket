"""
This module contains the routes for file operations.
"""

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

    file = flask.request.files["file"]
    config.s3.upload_fileobj(file, bucket, file.filename)

    return "Uploaded file successfully.", 201


@blueprint.route("/<bucket>/<filename>", methods=["GET"])
@decorators.format_response
def download(bucket, filename):
    """
    Fetches a file from the specified bucket.
    """

    try:
        config.s3.download_file(bucket, filename, filename)

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

        return "Deleted file successfully.", 200
    except Exception as error:
        return str(error), 404
