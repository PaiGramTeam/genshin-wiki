from typing import Type, TypeVar

import ujson as json
from pydantic import (
    BaseConfig as PydanticBaseConfig,
    BaseModel as PydanticBaseModel,
    BaseSettings as PydanticBaseSettings,
)

__all__ = ("BaseConfig", "BaseSettings", "BaseModel")

T = TypeVar("T")


class BaseConfig(PydanticBaseConfig):
    json_dumps = json.dumps
    json_loads = json.loads


class BaseSettings(PydanticBaseSettings):
    def __new__(cls: Type[T], *args, **kwargs) -> T:
        cls.update_forward_refs()
        return super(PydanticBaseSettings, cls).__new__(cls)

    class Config(BaseConfig):
        pass


class BaseModel(PydanticBaseModel):
    def __new__(cls: Type[T], *args, **kwargs) -> T:
        cls.update_forward_refs()
        return super(PydanticBaseModel, cls).__new__(cls)

    class Config(BaseConfig):
        pass
