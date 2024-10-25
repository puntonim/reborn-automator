from aws_lambda_powertools import Logger

from ..__version__ import __version__

logger = Logger(
    service=f"reborn automator v{__version__}",
    location="%(pathname)s::%(funcName)s::%(lineno)d",
    # logger_handler=handler,  # TODO To be used in tests, eg. `caplog.handler`, not sure!?
)
