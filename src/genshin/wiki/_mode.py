from typing import TYPE_CHECKING, TypeVar

import peewee
from peewee import CharField, SqliteDatabase
from peewee_async import MySQLDatabase

from genshin.wiki.config import genshin_wiki_config

if TYPE_CHECKING:
    from peewee import Database

__all__ = (
    "Model",
    "ModelMeta",
)


T = TypeVar("T")


database = MySQLDatabase(genshin_wiki_config.database_url)
database.connect()

class ModelMeta:
    database: "Database" = database


class Model(peewee.Model):
    class Meta(ModelMeta):
        abstract = True

class MapStringField(CharField):

    def db_value(self, value):
        return value.hex  # convert UUID to hex string.

    def python_value(self, value):
        return value
