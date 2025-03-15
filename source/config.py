"""
This file contains the configuration for the application.
"""

import os


class BaseConfig:
    """
    This class contains the configuration for the application.
    """

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID")
    AWS_CLOUDWATCH_LOGS_ENDPOINT = os.getenv("AWS_CLOUDWATCH_LOGS_ENDPOINT")
    AWS_CLOUDWATCH_LOGS_LOG_GROUP = os.getenv("AWS_CLOUDWATCH_LOGS_LOG_GROUP")
    AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
    AWS_S3_ENDPOINT = os.getenv("AWS_S3_ENDPOINT")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS").split(",")
    ENVIRONMENT = os.getenv("ENVIRONMENT")

    DEBUG = False
    SECRET_KEY = AWS_SECRET_ACCESS_KEY
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """
    This class contains the development configuration for the application.
    """

    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    """
    This class contains the testing configuration for the application.
    """

    DEBUG = False
    TESTING = True


class ProductionConfig(BaseConfig):
    """
    This class contains the production configuration for the application.
    """

    DEBUG = False
    TESTING = False
