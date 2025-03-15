"""
Decorators for the API.
"""

import functools
import typing

import botocore
import flask


def format_response(callback: typing.Callable):
    """
    Formats the response of the API.

    :param typing.Callable callback: The wrapped function. The first returned element is
        the message, the second is the status code, and the third is a keyword dictionary,
        which contains an optional element `data`.
    :return: The formatted JSON response.
    :rtype: flask.Response
    """

    @functools.wraps(callback)
    def inner(*args, **kwargs):
        try:
            message, status, *data = callback(*args, **kwargs)
            payload = {"message": message}
            if data:
                payload["data"] = data[0]
            return (flask.jsonify(payload), status)
        except botocore.exceptions.ClientError as error:
            flask.current_app.config["service_logger"].error(
                "%s triggered an client error.",
                flask.request.remote_addr,
                exc_info=True,
            )
            return (
                flask.jsonify(
                    {"message": f"{error.__class__.__name__}: {error.args[0]}"}
                ),
                500,
            )
        # pylint: disable=broad-exception-caught
        except Exception as error:
            flask.current_app.config["default_logger"].error(
                "%s triggered an server error.",
                flask.request.remote_addr,
                exc_info=True,
            )
            return (
                flask.jsonify(
                    {"message": f"{error.__class__.__name__}: {error.args[0]}"}
                ),
                500,
            )

    return inner
