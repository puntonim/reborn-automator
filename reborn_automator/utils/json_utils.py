import json
from datetime import datetime
from uuid import UUID


class CustomJsonEncoder(json.JSONEncoder):
    """
    Usage:
        json.dumps(data, cls=CustomJsonEncoder)
    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif obj.__class__.__name__ == "Decimal":
            # It's the Decimal class coming from DynamoDB and
            #  we don't want to import its lib, so we check for the
            #  class name.
            return float(obj)
        elif obj.__class__.__name__ == "Url":
            # It's the pydantic.HttpUrl class coming from pydantic and
            #  we don't want to import its lib, so we check for the
            #  class name.
            return str(obj)
        elif hasattr(obj, "to_dict") and callable(obj.to_dict):
            return obj.to_dict()
        elif isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def to_json(data, sort_keys=False, **kwargs):
    return json.dumps(data, cls=CustomJsonEncoder, sort_keys=sort_keys, **kwargs)
