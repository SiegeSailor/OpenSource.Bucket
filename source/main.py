"""
This module contains the main application logic.
"""

import decorators
import flask
import flask_cors
import routes

main = flask.Flask(import_name=__name__)
flask_cors.CORS(app=main)

main.register_blueprint(blueprint=routes.file.blueprint)


@main.route("/", methods=["GET"])
@decorators.format_response
def check():
    """
    Check if the application is running.
    """

    return "The service is running.", 200
