"""
This module contains the main application logic.
"""

import flask
import flask_cors

import source.config
import source.decorators
import source.route


def create_main():
    """
    Create the main application object.
    """

    main = flask.Flask(import_name=__name__)
    main.config.from_object(
        {
            "development": source.config.DevelopmentConfig,
            "testing": source.config.TestingConfig,
            "production": source.config.ProductionConfig,
        }[source.config.Environment.ENVIRONMENT]
    )

    flask_cors.CORS(app=main)

    main.register_blueprint(blueprint=source.route.file.blueprint)

    @main.route("/", methods=["GET"])
    @source.decorators.format_response
    def check():
        """
        Check if the application is running.
        """

        return "The service is running.", 200

    @main.errorhandler(404)
    @source.decorators.format_response
    def fallback(_):
        """
        Fallback route for handling 404 errors.
        """

        return f"Route {flask.request.path} does not exist.", 404

    return main
