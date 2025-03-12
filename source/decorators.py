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
            message, status, *data = callback(*args, **kwargs)
            return (
                flask.jsonify(
                    {
                        "message": message,
                        "data": data[0] if data else {},
                    }
                ),
                status,
            )
        # pylint: disable=broad-exception-caught
        except Exception as error:
            return (
                flask.jsonify(
                    {
                        "message": "Failed to execute the operation.",
                        "data": {"error": str(error)},
                    }
                ),
                500,
            )

    return inner
