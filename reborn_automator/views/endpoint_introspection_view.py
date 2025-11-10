import importlib
import sqlite3
import sys
from typing import Any

import datetime_utils
import log_utils as logger
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEventV2
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_utils import aws_lambda_utils

from ..__version__ import __version__
from ..conf import settings
from .views_utils import lambda_static_init

# Objects declared outside the Lambda's handler method are part of Lambda's
# *execution environment*. This execution environment is sometimes reused for subsequent
# function invocations. Note that you can not assume that this always happens.
# Typical use cases: database connection and log init. The same db connection can be
# re-used in some subsequent function invocations. It is recommended though to add
# logic to check if a connection already exists before creating a new one.
# The execution environment also provides 512 MB of *disk space* in the /tmp directory.
# Again, this can be re-used in some subsequent function invocations.
# See: https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html#static-initialization

# This Lambda is configured with 0 retries. So do raise exceptions in the view.

lambda_static_init()

logger.info("ENDPOINT INTROSPECTION: LOADING")


@logger.get_adapter().inject_lambda_context(log_event=True)
def lambda_handler(event: dict[str, Any], context: LambdaContext) -> dict:
    """
    Get introspection info.

    Args:
        event: an AWS event, eg. Lambda URL or API Gateway invocation.
        context: the context passed to the Lambda.

    The `event` is a dict (that can be casted to `APIGatewayProxyEventV2`) like:
        {
            "version": "2.0",
            "routeKey": "GET /version",
            "rawPath": "/version",
            "rawQueryString": "",
            "headers": {
                "accept": "*/*",
                "content-length": "0",
                "host": "tr7lfzd0ec.execute-api.eu-south-1.amazonaws.com",
                "user-agent": "curl/7.87.0",
                "x-amzn-trace-id": "Root=1-64590511-3e02d77463e0d98e773b22d6",
                "x-forwarded-for": "151.55.81.75",
                "x-forwarded-port": "443",
                "x-forwarded-proto": "https"
            },
            "requestContext": {
                "accountId": "477353422995",
                "apiId": "tr7lfzd0ec",
                "domainName": "tr7lfzd0ec.execute-api.eu-south-1.amazonaws.com",
                "domainPrefix": "tr7lfzd0ec",
                "http": {
                    "method": "GET",
                    "path": "/version",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "151.55.81.75",
                    "userAgent": "curl/7.87.0"
                },
                "requestId": "Em261gw4su8EMww=",
                "routeKey": "GET /version",
                "stage": "$default",
                "time": "08/May/2023:14:20:01 +0000",
                "timeEpoch": 1683555601890
            },
            "isBase64Encoded": false
        }

    The `context` is a `LambdaContext` instance with properties similar to:
        {
            "aws_request_id": "e23b50d7-f384-4954-b6b5-395ec8faffce",
            "log_group_name": "/aws/lambda/contabel-prod-endpoint-introspection",
            "log_stream_name": "2023/04/18/[$LATEST]1de9ef8decd54172a43cfe6bea75731c",
            "function_name": "contabel-prod-endpoint-introspection",
            "memory_limit_in_mb": "256",
            "function_version": "$LATEST",
            "invoked_function_arn": "arn:aws:lambda:eu-south-1:477353422995:function:contabel-prod-endpoint-introspection",
            "client_context": null,
            "identity": "CognitoIdentity([cognito_identity_id=None,cognito_identity_pool_id=None])",
            "_epoch_deadline_time_in_ms": 1681848368843
        }
    More info here: https://docs.aws.amazon.com/lambda/latest/dg/python-context.html

    Example:
        $ curl https://tr7lfzd0ec.execute-api.eu-south-1.amazonaws.com/health
        "2023-04-18T19:56:45.219316+00:00"
    """
    logger.info("ENDPOINT INTROSPECTION: START")

    api_event = APIGatewayProxyEventV2(event)

    if api_event.path.endswith("/version"):
        data = {
            "appName": settings.APP_NAME,
            "app": __version__,
            "python": sys.version,
            "boto3": None,
            "botocore": None,
            "pydantic": None,
            "sqlite3": sqlite3.sqlite_version,
        }

        try:
            boto3 = importlib.import_module("boto3")
            data["boto3"] = boto3.__version__
        except ImportError:
            pass
        try:
            botocore = importlib.import_module("botocore")
            data["botocore"] = botocore.__version__
        except ImportError:
            pass
        try:
            pydantic = importlib.import_module("pydantic")
            data["pydantic"] = [
                x.strip() for x in pydantic.version.version_info().split("\n")
            ]
        except ImportError:
            pass

        return aws_lambda_utils.Ok200Response(data).to_dict()

    if api_event.path.endswith("/health"):
        now = datetime_utils.now_utc().isoformat()
        logger.debug("Debug log entry")
        logger.info("Info log entry")
        # Commented out otherwise they trigger `cloudwatch-error-email` Lambda to
        #  send an email.
        # logger.warning("Warning log entry")
        # logger.error("Error log entry")
        # logger.critical("Critical log entry")
        return aws_lambda_utils.Ok200Response(now).to_dict()

    if api_event.path.endswith("/unhealth"):
        now = datetime_utils.now_utc().isoformat()
        logger.debug("Debug log entry")
        logger.info("Info log entry")
        logger.warning("Warning log entry")
        logger.error("Error log entry")
        logger.critical("Critical log entry")
        raise UnhealthEndpointException(ts=now)

    return aws_lambda_utils.NotFound404Response().to_dict()


class UnhealthEndpointException(Exception):
    def __init__(self, ts: str):
        self.ts = ts
