
from pathlib import Path

from pydantic import BaseModel

from genshin_wiki.tools.const import DATA_DIR
from genshin_wiki.tools.typedefs import Lang
from contextlib import contextmanager

__all__ = (
    "genshin_wiki_config",
    "with_genshin_wiki_config",
)


class _GenshinWikiConfig(BaseModel):
    lang: Lang = "chs"

    database_path: Path = DATA_DIR.joinpath('database.sqlite')

    request_timeout: int = 10
    request_retry_times: int = 5

    metadata_link: str = "https://gitlab.com/Dimbreath/AnimeGameData/-/raw/master/"


genshin_wiki_config = _GenshinWikiConfig()


@contextmanager
def with_genshin_wiki_config(**kwargs):
    global genshin_wiki_config
    old_config = genshin_wiki_config
    config_dict = genshin_wiki_config.dict()
    config_dict.update(kwargs)
    genshin_wiki_config = _GenshinWikiConfig(**config_dict)
    yield
    genshin_wiki_config = old_config
