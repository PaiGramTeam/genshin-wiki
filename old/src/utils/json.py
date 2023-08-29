from typing import Any
from datetime import datetime
from json import JSONEncoder as _JSONEncoder

from orjson import dumps as json_dumps
from orjson import loads as json_loads
from orjson import JSONDecodeError as _JSONDecodeError
from orjson import JSONEncodeError as _JSONEncodeError

__all__ = ("JSONEncodeError", "JSONDecodeError", "dumps", "loads")

JSONEncodeError = _JSONEncodeError
JSONDecodeError = _JSONDecodeError


def _default(value: Any):
    if isinstance(value, datetime):
        return value.timestamp()
    return value


def loads(*args, **kwargs) -> Any:
    return json_loads(*args, **kwargs)


def dumps(*args, **kwargs) -> str:
    default = kwargs.pop("default", _default)
    return json_dumps(*args, default=default, **kwargs).decode(encoding="utf-8")


class JSONEncoder(_JSONEncoder):
    pass
