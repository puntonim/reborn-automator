import sqlite3
import sys
from typing import Any

import boto3
import botocore
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEventV2
from aws_lambda_powertools.utilities.typing import LambdaContext

from ..__version__ import __version__
from ..conf import settings
from ..utils import aws_lambda_utils, datetime_utils
from ..utils.log_utils import logger

# Objects declared outside the Lambda's handler method are part of Lambda's
# *execution environment*. This execution environment is sometimes reused for subsequent
# function invocations. Note that you can not assume that this always happens.
# Typical use case: database connection. The same connection can be re-used in some
# subsequent function invocations. It is recommended though to add logic to check if a
# connection already exists before creating a new one.
# The execution environment also provides 512 MB of *disk space* in the /tmp directory.
# Again, this can be re-used in some subsequent function invocations.
# See: https://docs.aws.amazon.com/lambda/latest/dg/runtimes-context.html#runtimes-lifecycle-shutdown

# The Lambda is configured with 0 retries. So do raise exceptions in the view.


logger.info("ENDPOINT INTROSPECTION: LOADING")


@logger.inject_lambda_context(log_event=True)
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

    # Mind that there is also a /admin/introspection endpoint that includes all
    #  this endpoints plus extra endpoints that expose some private info.

    if api_event.path.endswith("/version"):
        body = {
            "appName": settings.APP_NAME,
            "app": __version__,
            "python": sys.version,
            "boto3": boto3.__version__,
            "botocore": botocore.__version__,
            "sqlite3": sqlite3.version,
        }
        return aws_lambda_utils.Ok200Response(body).to_dict()

    if api_event.path.endswith("/echo"):
        body = {
            "url": api_event.raw_path,
            "queryStringParameters": api_event.query_string_parameters or dict(),
            "method": api_event.http_method,
            "headers": api_event.headers,
        }
        return aws_lambda_utils.Ok200Response(body).to_dict()

    if api_event.path.endswith("/health"):
        now = datetime_utils.now_utc().isoformat()
        logger.debug("Debug log entry")
        logger.info("Info log entry")
        logger.warning("Warning log entry")
        logger.error("Error log entry")
        logger.critical("Critical log entry")
        return aws_lambda_utils.Ok200Response(now).to_dict()

    if api_event.path.endswith("/unhealth"):
        now = datetime_utils.now_utc().isoformat()
        logger.debug("Debug log entry")
        logger.info("Info log entry")
        logger.warning("Warning log entry")
        logger.error("Error log entry")
        logger.critical("Critical log entry")
        raise UnhealthCommandException(ts=now)

    return aws_lambda_utils.NotFound404Response().to_dict()


class UnhealthCommandException(Exception):
    def __init__(self, ts: str):
        self.ts = ts
