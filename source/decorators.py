"""
Decorators for the API.
"""

import functools

import flask


def format_response(callback):
    """
    Formats the response of the API.
    """

    @functools.wraps(callback)
    def inner(*args, **kwargs):
        try:
            message, status = callback(*args, **kwargs)
            return (flask.jsonify({"message": message}), status)
        # pylint: disable=broad-exception-caught
        except Exception as error:
            return (flask.jsonify({"message": str(error)}), 500)

    return inner
