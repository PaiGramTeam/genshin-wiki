import os
from datetime import datetime

# noinspection PyPep8Naming
from enum import Enum as E
from pathlib import Path
from typing import Any, Type

# noinspection PyPep8Naming
from ormar import (
    BaseField,
    Enum as ENUM,
    String as STRING,
)

try:
    import regex as re
except ImportError:
    import re

import databases
import ormar
import sqlalchemy
import ujson as json
from pydantic import BaseConfig

from tools.const import OUTPUT_DIR

__all__ = (
    "database_url",
    "engine",
    "databases",
    "metadata",
    "Model",
    "ModelMeta",
    "Enum",
    "String",
)


database_url = (
    "sqlite:///"
    f"{OUTPUT_DIR.joinpath(os.environ.get('LANG', 'chs')).joinpath('database.sqlite').resolve()}"
).replace("\\", "/")

engine = sqlalchemy.create_engine(
    database_url, json_serializer=json.dumps, json_deserializer=json.loads
)
database = databases.Database(database_url)
metadata = sqlalchemy.MetaData(engine)


class ModelMeta(ormar.ModelMeta):
    database = database
    metadata = metadata


class ModelConfig(BaseConfig):
    json_encoders = {datetime: lambda v: v.timestamp()}
    json_loads = json.loads
    json_dumps = json.dumps


class Model(ormar.Model):
    class Config(ModelConfig):
        pass

    class Meta(ModelMeta):
        abstract = True


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
