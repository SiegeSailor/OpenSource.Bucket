"""
This module contains the routes for file operations.
"""

import flask

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

    url = source.controller.file.upload_file(
        client=flask.current_app.config["client_s3"],
        file=file,
        bucket=bucket,
        logger=flask.current_app.config["logger_service"],
    )

    return "Uploaded file successfully.", 201, {"location": url}


@blueprint.route("/<bucket>/<filename>", methods=["GET"])
@source.decorator.format_response
def generate_url(bucket, filename):
    """
    Fetches a file from the specified bucket.
    """

    metadata = flask.current_app.config["client_s3"].head_object(
        Bucket=bucket, Key=filename
    )

    url = source.controller.file.generate_presigned_url(
        client=flask.current_app.config["client_s3"],
        bucket=bucket,
        filename=filename,
        content_type=metadata["ContentType"],
        logger=flask.current_app.config["logger_service"],
    )

    return "Generated file URL successfully.", 200, {"location": url}


@blueprint.route("/<bucket>/<filename>", methods=["DELETE"])
@source.decorator.format_response
def delete_file(bucket, filename):
    """
    Deletes a file from the specified bucket.
    """

    source.controller.file.delete_file(
        client=flask.current_app.config["client_s3"],
        bucket=bucket,
        filename=filename,
        logger=flask.current_app.config["logger_service"],
    )

    return "Deleted file successfully.", 200
