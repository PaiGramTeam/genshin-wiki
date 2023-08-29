import os
from functools import lru_cache
from logging import getLogger
from pathlib import Path

import httpx
import ujson as json
from httpx import Client
from yarl import URL

from genshin_wiki.config import genshin_wiki_config
from genshin_wiki.tools.const import DATA_DIR
from genshin_wiki.tools.typedefs import Lang

__all__ = ("resource_manager",)

logger = getLogger(__name__)


class _ResourceManager:
    _client: Client

    _text_maps: dict[Lang, dict[str, str]] = {}

    @property
    def client(self) -> Client:
        if not hasattr(self, "_client"):
            self._client = Client(timeout=genshin_wiki_config.request_timeout)
        return self._client

    @lru_cache()
    def fetch_metadata(
        self,
        name: str,
        path: str = "ExcelBinOutput",
        *,
        output_dir: str | Path = DATA_DIR,
    ) -> dict:
        logger.debug(f"Resource Manager is fetching metadata: {name} of {path}, to {output_dir}")

        file_path = (
            Path(output_dir)
            .resolve()
            .joinpath(name)
            .with_suffix("")
            .with_suffix(".json")
        )
        file_path.parent.mkdir(exist_ok=True, parents=True)

        if not (file_path.exists() and os.stat(file_path)):
            times = 0
            while True:
                try:
                    response = self.client.get(
                        str(URL(genshin_wiki_config.metadata_link) / path / file_path.name)
                    )
                    break
                except httpx.RequestError as e:
                    if times < genshin_wiki_config.request_retry_times:
                        times += 1
                        continue
                    raise e
            # noinspection PyUnboundLocalVariable,PyUnresolvedReferences
            response.raise_for_status()
            with open(file_path, encoding="utf-8", mode="w") as file:
                file.write(content := response.text)
                return json.loads(content)

        with open(file_path, encoding="utf-8", mode="r") as file:
            return json.loads(file.read())

    @lru_cache(typed=True)
    def get_text(self, key: int | str | None) -> str | None:
        if key is None:
            return None
        _lang = genshin_wiki_config.lang
        if self._text_maps.get(_lang) is None:
            self._text_maps[_lang] = self.fetch_metadata("TextMap" + _lang.upper(), "TextMap")
        result = self._text_maps[_lang].get(str(key), None)
        if result is not None:
            return result.replace("\\n", "\n")
        return result

resource_manager = _ResourceManager()
