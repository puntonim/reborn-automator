import json
from typing import Any

from aws_lambda_powertools.utilities.typing import LambdaContext

from ..clients.botte_api_client import BotteApiClient
from ..domains.book_class_domain import (
    BookClassDomain,
    FailedBooking,
    NoCalisthenicsClassFoundInPalinsesto,
)
from ..utils import emoji_utils
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


logger.info("CRON BOOK CLASS: LOADING")


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict[str, Any], context: LambdaContext) -> None:
    """
    Book the next calisthenics class at Reborn.

    Args:
        event: an AWS event, eg. CloudWatch Scheduled Event.
        context: the context passed to the Lambda.

    The `event` is a dict (that can NOT be casted to any aws_lambda_powertools class) like:
        {
            "id": "cdc73f9d-aea9-11e3-9d5a-835b769c0d9c",
            "detail-type": "Scheduled Event",
            "source": "aws.events",
            "account": "123456789012",
            "time": "1970-01-01T00:00:00Z",
            "region": "us-east-1",
            "resources": [
                "arn:aws:events:us-east-1:123456789012:rule/ExampleRule"
            ],
            "detail": {}
        }

    The `context` is a `LambdaContext` instance with properties similar to:
        {
            "aws_request_id": "4eb14fcb-f0c7-4814-98fc-d92baaa7784f",
            "log_group_name": "/aws/lambda/patatrack-contabel-prod-cron-report",
            "log_stream_name": "2023/10/31/[$LATEST]df94460a2fb14d6480db01799b8b0d59",
            "function_name": "patatrack-contabel-prod-cron-report",
            "memory_limit_in_mb": "256",
            "function_version": "$LATEST",
            "invoked_function_arn": "arn:aws:lambda:eu-south-1:477353422995:function:patatrack-contabel-prod-cron-report",
            "client_context": null,
            "identity": "CognitoIdentity([cognito_identity_id=None,cognito_identity_pool_id=None])",
            "_epoch_deadline_time_in_ms": 1698779351968
        }
    More info here: https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
    """
    logger.info("CRON BOOK CLASS: START")

    # Note: there is no class in aws_lambda_powertools that represents CloudWatch
    #  Scheduled Event.

    domain = BookClassDomain()
    exception = None
    response = None
    day_date = None
    try:
        response, day_date = domain.book_next_calisthenics_class()
    except (FailedBooking, NoCalisthenicsClassFoundInPalinsesto) as exc:
        exception = exc
    except Exception as exc:
        exception = exc

    # Use Botte (from patatrack monorepo) to send a Telegram message.
    botte = BotteApiClient()

    if not exception:
        logger.info("Booking successful", extra=dict(response=response))
        botte.send_telegram_message(
            emoji_utils.MUSCLE
            + emoji_utils.GREEN_CIRCLE
            + "Calisthenics class booked for "
            + day_date.strftime("%Y-%m-%d")
        )

    if exception:
        exc_str = str(exception)
        extra = dict(exc=exc_str)
        message = emoji_utils.MUSCLE + emoji_utils.RED_CIRCLE

        if isinstance(exception, NoCalisthenicsClassFoundInPalinsesto):
            message += "Calisthenics class NOT found in palinsesto"
        else:
            if isinstance(exception, FailedBooking):
                extra = extra["response"] = exception.response
                day_date = exception.day_date
                exc_str = json.dumps(exception.response, indent=2)
            message += (
                "Calisthenics class NOT booked for "
                + day_date.strftime("%Y-%m-%d")
                # Botte only supports plain text now, so no formatting.
                # + '\n<pre><code class="language-json">\n'
                + "\n\n"
                + exc_str
            )

        logger.info("Booking error", extra=extra)
        botte.send_telegram_message(message)
        raise exception
