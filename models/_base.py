from humps import camelize

from utils.model import BaseConfig, BaseModel


class DataModel(BaseModel):
    class Config(BaseConfig):
        alias_generator = lambda x: camelize(x.removesuffix("TextHashMap"))
