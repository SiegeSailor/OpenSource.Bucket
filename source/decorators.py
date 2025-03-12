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
            payload = {"message": message}
            if data:
                payload["data"] = data[0]
            return (
                flask.jsonify(payload),
                status,
            )
        # pylint: disable=broad-exception-caught
        except Exception as error:
            return (
                flask.jsonify(
                    {
                        "message": str(error),
                    }
                ),
                500,
            )

    return inner
