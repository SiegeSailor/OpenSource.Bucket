"""
This module contains the main application logic.
"""

import logging
import os

import flask
import flask_cors

import source.client
import source.config
import source.decorator
import source.route


def register_client(main: flask.Flask):
    """
    Configure the main application object.
    """

    aws = source.client.AWS(
        region=main.config["AWS_DEFAULT_REGION"],
        secret_access_key=main.config["AWS_SECRET_ACCESS_KEY"],
        access_key_id=main.config["AWS_ACCESS_KEY_ID"],
        session_token=main.config["AWS_SESSION_TOKEN"],
        account_id=main.config["AWS_ACCOUNT_ID"],
    )

    main.config["s3"] = aws.create_client(
        service="s3",
        endpoint_url=main.config["AWS_S3_ENDPOINT"],
    )

    main.config["logs"] = aws.create_client(
        service="logs",
        endpoint_url=main.config["AWS_CLOUDWATCH_LOGS_ENDPOINT"],
    )
    main.config["service_logger"] = aws.create_logger(
        group=main.config["AWS_CLOUDWATCH_LOGS_LOG_GROUP"],
        stream="service",
        client=main.config["logs"],
        name="service",
    )
    main.config["default_logger"] = aws.create_logger(
        group=main.config["AWS_CLOUDWATCH_LOGS_LOG_GROUP"],
        stream="default",
        client=main.config["logs"],
        name=None,
    )


def create_main():
    """
    Create the main application object.
    """

    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])

    main = flask.Flask(import_name=__name__)
    main.config.from_object(
        {
            "development": source.config.DevelopmentConfig,
            "testing": source.config.TestingConfig,
            "production": source.config.ProductionConfig,
        }[os.getenv("ENVIRONMENT")]
    )

    register_client(main=main)

    flask_cors.CORS(app=main)

    main.register_blueprint(blueprint=source.route.file.blueprint)

    @main.route("/", methods=["GET"])
    @source.decorator.format_response
    def check():
        """
        Check if the application is running.
        """

        return "The service is running.", 200

    @main.errorhandler(404)
    @source.decorator.format_response
    def fallback(_):
        """
        Fallback route for handling 404 errors.
        """

        return f"Route {flask.request.path} does not exist.", 404

    return main
