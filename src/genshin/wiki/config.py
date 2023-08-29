import inspect
from contextlib import contextmanager
from typing import Any, Generator

from pydantic_settings import BaseSettings

from genshin.wiki.tools.typedefs import Lang

__all__ = ("genshin_wiki_config", "use_genshin_wiki_config")


class _GenshinWikiConfig(BaseSettings, env_prefix='genshin_wiki_'):
    lang: Lang = "chs"
    """Language of the data to be used."""

    database_url: str = "mysql://root:123456@localhost:3306/genshin_wiki?charset=utf8mb4"
    """The connection url of the database."""

    metadata_repo: str = "https://gitlab.com/Dimbreath/AnimeGameData/"
    """The repo link of the GenshinData."""

genshin_wiki_config = _GenshinWikiConfig()


@contextmanager
def use_genshin_wiki_config(**kwargs) -> Generator[_GenshinWikiConfig, Any, None]:
    global genshin_wiki_config
    old_config = genshin_wiki_config
    config_dict = genshin_wiki_config.model_dump()
    config_dict.update(kwargs)
    new_config = _GenshinWikiConfig(**config_dict)

    frame = inspect.currentframe().f_back.f_back

    local_keys = []
    for k, v in frame.f_locals.items():
        if type(v).__name__ == _GenshinWikiConfig.__name__:
            frame.f_locals[k] = new_config
            local_keys.append(k)
    global_keys = []
    for k, v in frame.f_globals.items():
        if type(v).__name__ == _GenshinWikiConfig.__name__:
            frame.f_globals[k] = new_config
            global_keys.append(k)

    genshin_wiki_config = _GenshinWikiConfig(**config_dict)

    yield genshin_wiki_config

    genshin_wiki_config = old_config

    for k in local_keys:
        frame.f_locals[k] = old_config
    for k in global_keys:
        frame.f_globals[k] = old_config
