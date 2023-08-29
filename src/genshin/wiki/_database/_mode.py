from pathlib import Path

import peewee
from peewee import IntegerField, SqliteDatabase

from genshin.wiki.config import get_wiki_lang
from genshin.wiki.tools.const import DATA_DIR
from genshin.wiki.tools.typedefs import Lang
from genshin.wiki.utils import LimitedSizeDict

__all__ = (
    "Model",
    "ModelMeta",
    "MapString",
    "MapStringField",
)


_database = SqliteDatabase(Path(__file__).joinpath('../sqlite.db'))
_database.connect()

_lang_database_map: LimitedSizeDict[Lang, SqliteDatabase] = LimitedSizeDict(size_limit=256)

class ModelMeta:
    database: SqliteDatabase = _database


class Model(peewee.Model):
    class Meta(ModelMeta):
        abstract = True

_map_string_cache: dict[int, "MapString"] = {}

class MapString(str):
    __slots__ = ("_text_id", "_lang")

    def __new__(cls, target: int | str) -> "MapString":
        lang = get_wiki_lang()

        _map_string_cache_key = hash((str(lang), target,))
        result = _map_string_cache.get(_map_string_cache_key, None)
        if result is not None:
            return result

        if lang not in _lang_database_map:
            database = SqliteDatabase(DATA_DIR.joinpath(lang + '.db').resolve())
            database.connect()
            _lang_database_map[lang] = database
        else:
            database = _lang_database_map[lang]

        if isinstance(target, int):
            text_id = target
            text = database.execute_sql(
                "SELECT context FROM mapping_text WHERE id = ?", (target,)
            ).fetchone()[0]
        else:
            text = target
            text_id = database.execute_sql(
                "SELECT id FROM mapping_text WHERE context = ?", (target,)
            ).fetchone()[0]
        
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

class MapStringField(IntegerField):

    def db_value(self, value: str | int | MapString) -> int:
        return MapString(value).text_id

    def python_value(self, value: int) -> MapString:
        return MapString(value)
