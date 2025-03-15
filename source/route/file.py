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
        s3_client=flask.current_app.config["s3"],
        logger=flask.current_app.config["service_logger"],
        file=file,
        bucket=bucket,
        is_replacing=flask.current_app.config["ENVIRONMENT"] == "development",
    )

    return "Uploaded file successfully.", 201, {"location": url}


@blueprint.route("/<bucket>/<filename>", methods=["GET"])
@source.decorator.format_response
def generate_url(bucket, filename):
    """
    Fetches a file from the specified bucket.
    """

    metadata = flask.current_app.config["s3"].head_object(Bucket=bucket, Key=filename)

    url = source.controller.file.generate_presigned_url(
        s3_client=flask.current_app.config["s3"],
        logger=flask.current_app.config["service_logger"],
        bucket=bucket,
        filename=filename,
        content_type=metadata["ContentType"],
        is_replacing=flask.current_app.config["ENVIRONMENT"] == "development",
    )

    return "Generated file URL successfully.", 200, {"location": url}


@blueprint.route("/<bucket>/<filename>", methods=["DELETE"])
@source.decorator.format_response
def delete(bucket, filename):
    """
    Deletes a file from the specified bucket.
    """

    source.controller.file.delete_file(
        s3_client=flask.current_app.config["s3"],
        logger=flask.current_app.config["service_logger"],
        bucket=bucket,
        filename=filename,
    )

    return "Deleted file successfully.", 200
