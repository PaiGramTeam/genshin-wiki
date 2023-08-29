from peewee import SqliteDatabase
from typing import Any

import orjson as json
from aiofiles import open as async_open
from pydantic import Json

from genshin.wiki.config import get_wiki_lang
from genshin.wiki.tools.const import DATA_DIR
from genshin.wiki.tools.typedefs import Lang
from genshin.wiki.utils.funcs import get_repo_raw
from genshin.wiki.utils.net import Net

LANG_DATA_DIR = DATA_DIR.joinpath("lang")
database_map: dict[Lang, SqliteDatabase] = {}
