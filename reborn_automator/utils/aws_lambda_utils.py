import json
import logging
from abc import ABC

from . import json_utils

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class BaseJsonResponse(ABC):
    STATUS_CODE = 200

    def __init__(
        self,
        body: str | dict | list | None = None,
        do_convert_to_json=True,
        status_code: int | None = None,
    ):
        self.body = body
        self.do_convert_to_json = do_convert_to_json
        self.status_code = status_code

    def to_dict(self) -> dict:
        status_code = self.status_code or self.STATUS_CODE
        response = dict()
        response["statusCode"] = status_code
        if self.body:
            response["Content-Type"] = "application/json"
            response["body"] = (
                json_utils.to_json(self.body) if self.do_convert_to_json else self.body
            )

        # Log the response only if not a 2XX.
        extra = None
        if status_code > 299:
            extra = dict(response=response)

        # Log with error level or info level.
        if status_code > 499:
            logger.error(f"Responding {status_code}")
        else:
            logger.info(f"Responding {status_code}")
        return response


class BadRequest400Response(BaseJsonResponse):
    STATUS_CODE = 400


class Unauthorized401Response(BaseJsonResponse):
    STATUS_CODE = 401


class NotFound404Response(BaseJsonResponse):
    STATUS_CODE = 404


class InternalServerError500Response(BaseJsonResponse):
    STATUS_CODE = 500


class Ok200Response(BaseJsonResponse):
    STATUS_CODE = 200


class Created201Response(BaseJsonResponse):
    STATUS_CODE = 201
