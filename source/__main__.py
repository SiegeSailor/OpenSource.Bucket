"""
This module contains the main application logic.
"""

import flask
import routes

application = flask.Flask(import_name=__name__)

application.register_blueprint(blueprint=routes.file.blueprint)


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
