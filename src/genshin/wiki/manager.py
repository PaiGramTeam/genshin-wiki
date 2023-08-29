from peewee import SqliteDatabase
from typing import Any

import orjson as json
from aiofiles import open as async_open
from pydantic import Json

from genshin.wiki.config import genshin_wiki_config
from genshin.wiki.tools.const import DATA_DIR
from genshin.wiki.tools.typedefs import Lang
from genshin.wiki.utils.funcs import get_repo_raw
from genshin.wiki.utils.net import Net

LANG_DATA_DIR = DATA_DIR.joinpath("lang")
database_map: dict[Lang, SqliteDatabase] = {}


class MappingText:
    _id: int | None = None
    _context: str | None = None

    def __init__(self, target: int | str) -> None:
        if genshin_wiki_config.lang not in database_map:
            self._database = SqliteDatabase(
                f"sqlite:///{LANG_DATA_DIR.joinpath(genshin_wiki_config.lang)}.sqlite"
            )
            database_map[genshin_wiki_config.lang] = self._database
        else:
            self._database = database_map[genshin_wiki_config.lang]

        if isinstance(target, int):
            self._id = target
            self._context = self._database.execute_sql(
                "SELECT context FROM mapping_text WHERE id = ?", (target,)
            ).fetchone()[0]
        else:
            self._context = target
            self._id = self._database.execute_sql(
                "SELECT id FROM mapping_text WHERE context = ?", (target,)
            ).fetchone()[0]

    def __eq__(self, other) -> bool:
        if isinstance(other, MappingText):
            return self._id == other._id
        return False

    def __hash__(self) -> int:
        return self._id


class ResourceManager(Net):
    @property
    def lang(self) -> Lang:
        return genshin_wiki_config.lang

    async def metadata(
        self, file_path: str, *, overwritten: bool = False
    ) -> Json[dict[str, Any]]:
        """Download metadata from the GenshinData repo."""
        url = get_repo_raw(genshin_wiki_config.metadata_repo) + file_path
        if (path := DATA_DIR.joinpath(file_path)).exists():
            if not overwritten:
                async with async_open(path, "r") as f:
                    return json.loads(await f.read())
            else:
                async with async_open(path, "w") as f:
                    async with await self._get(url) as resp:
                        await f.write(await resp.text())
                    return await resp.json()

    async def text(self, text_id: int) -> str:
        ...
