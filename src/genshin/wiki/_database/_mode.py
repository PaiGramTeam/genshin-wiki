from pathlib import Path

import peewee
from peewee import CharField, IntegerField, SqliteDatabase

from genshin.wiki.config import get_wiki_lang
from genshin.wiki.tools.const import DATA_DIR
from genshin.wiki.tools.typedefs import Lang
from genshin.wiki.utils import LimitedSizeDict

__all__ = (
    "Model",
    "ModelMeta",
    "MappingTextModel",
    "MapText",
    "MapTextField",
)


_database = SqliteDatabase(Path(__file__).joinpath('../sqlite.db'))
_database.connect()

_text_database = SqliteDatabase(DATA_DIR.joinpath('text.db').resolve())

class ModelMeta:
    database: SqliteDatabase = _database


class Model(peewee.Model):
    class Meta(ModelMeta):
        abstract = True


class MappingTextModel(peewee.Model):
    class Meta:
        database= _text_database

    id = IntegerField(primary_key=True)
    text_id = IntegerField()
    context = CharField()
    lang = CharField()

_map_string_cache: dict[int, "MapText"] = LimitedSizeDict(size_limit=256)

class MapText(str):
    __slots__ = ("_text_id", "_lang")

    def __new__(cls, target: int | str) -> "MapText":
        lang = get_wiki_lang()

        _map_string_cache_key = hash((str(lang), target))
        result = _map_string_cache.get(_map_string_cache_key, None)
        if result is not None:
            return result

        if isinstance(target, int):
            text_id = target
            model = MappingTextModel.get_or_none(text_id=text_id, lang=lang)
            text = model.context if model is not None else ""
        else:
            text = target
            model = MappingTextModel.get_or_none(context=text, lang=lang)
            text_id = model.text_id if model is not None else 0

        result = super().__new__(cls, text)
        result._text_id = text_id
        result._lang = lang

        _map_string_cache[_map_string_cache_key] = result

        return result

    @property
    def lang(self) -> Lang:
        return self._lang

    @property
    def text_id(self) -> int:
        return self._text_id

class MapTextField(IntegerField):

    def db_value(self, value: str | int | MapText) -> int:
        return MapText(value).text_id

    def python_value(self, value: int) -> MapText:
        return MapText(value)
