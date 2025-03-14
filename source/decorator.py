"""
Decorators for the API.
"""

import functools
import typing

import botocore
import flask

import source.client


def format_response(callback: typing.Callable):
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
        except botocore.exceptions.ClientError:
            source.client.logs_logger.error(
                "%s encountered an error.",
                flask.request.remote_addr,
                exc_info=True,
            )
            raise
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
