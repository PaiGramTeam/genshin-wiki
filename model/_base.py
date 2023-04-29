from datetime import datetime

# noinspection PyPep8Naming
from enum import Enum as E
from typing import Any, TYPE_CHECKING, Type

from databases import Database

# noinspection PyPep8Naming
from ormar import (
    BaseField,
    Enum as ENUM,
    Model as _Model,
    ModelMeta as _ModelMeta,
    String as STRING,
)
from sqlalchemy import MetaData

from utils import json

try:
    import regex as re
except ImportError:
    import re

if TYPE_CHECKING:
    pass

__all__ = ("Model", "String", "Enum")

DATABASE_URL = "sqlite:///data/db.sqlite"
database = Database(DATABASE_URL)
metadata = MetaData()


class ModelMeta(_ModelMeta):
    database = database
    metadata = metadata


class Model(_Model):
    class Config(_Model.Config):
        json_dumps = json.dumps
        json_loads = json.loads
        json_encoders = {datetime: lambda v: v.timestamp()}


class String(STRING):
    def __new__(
        cls,
        *,
        max_length: int = 255,
        min_length: int = None,
        regex: str = None,
        **kwargs: Any,
    ) -> BaseField:
        return super().__new__(
            cls=STRING,
            max_length=max_length,
            min_length=min_length,
            regex=regex,
            **kwargs,
        )


class Enum(ENUM):
    def __new__(cls, enum_class: Type[E], **kwargs: Any) -> BaseField:
        return super().__new__(
            cls,
            **{
                **kwargs,
                **{
                    k: v
                    for k, v in locals().items()
                    if k not in ["cls", "__class__", "kwargs"]
                },
            },
        )
