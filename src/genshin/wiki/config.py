from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Generator, Optional, TYPE_CHECKING

from pydantic import PrivateAttr
from pydantic_settings import BaseSettings

from genshin.wiki.tools.typedefs import Lang

if TYPE_CHECKING:
    from contextvars import Token

__all__ = ("set_wiki_lang", "get_wiki_lang",)


class _GenshinWikiConfig(BaseSettings, env_prefix='genshin_wiki_'):
    _token: Optional["Token"] = PrivateAttr(None)

    lang: Lang = "chs"
    """Language of the data to be used."""

    metadata_repo: str = "https://gitlab.com/Dimbreath/AnimeGameData/"
    """The repo link of the GenshinData."""

_genshin_wiki_config = _GenshinWikiConfig()
_genshin_wiki_lang: ContextVar[Lang] = ContextVar('_genshin_wiki_lang', default=_genshin_wiki_config.lang)

@contextmanager
def set_wiki_lang(lang: Lang) -> Generator[_GenshinWikiConfig, Any, None]:
    token = _genshin_wiki_lang.set(lang)
    config = _GenshinWikiConfig(lang=lang, metadata_repo=_genshin_wiki_config.metadata_repo)
    try:
        yield config
    finally:
        _genshin_wiki_lang.reset(token)

def get_wiki_lang() -> Lang:
    return _genshin_wiki_lang.get()

# @contextmanager
# def use_genshin_wiki_config(**kwargs) -> "Generator[_GenshinWikiConfig, Any, None]":
#     import inspect
#     from contextlib import contextmanager
#     global genshin_wiki_config
#     old_config = genshin_wiki_config
#     config_dict = genshin_wiki_config.model_dump()
#     config_dict.update(kwargs)
#     new_config = _GenshinWikiConfig(**config_dict)
#
#     frame = inspect.currentframe().f_back.f_back
#
#     local_keys = []
#     for k, v in frame.f_locals.items():
#         if type(v).__name__ == _GenshinWikiConfig.__name__:
#             frame.f_locals[k] = new_config
#             local_keys.append(k)
#     global_keys = []
#     for k, v in frame.f_globals.items():
#         if type(v).__name__ == _GenshinWikiConfig.__name__:
#             frame.f_globals[k] = new_config
#             global_keys.append(k)
#
#     genshin_wiki_config = _GenshinWikiConfig(**config_dict)
#
#     yield genshin_wiki_config
#
#     genshin_wiki_config = old_config
#
#     for k in local_keys:
#         frame.f_locals[k] = old_config
#     for k in global_keys:
#         frame.f_globals[k] = old_config
