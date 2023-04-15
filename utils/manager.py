import os
import ssl
from functools import lru_cache

import ujson as json
from httpx import Client
from pydantic import Json
from yarl import URL

from utils.const import DATA_DIR
from utils.single import Singleton
from utils.typedefs import Lang

__all__ = "ResourceManager"

ssl_context = ssl.SSLContext()


class ResourceManager(Singleton):
    _lang: Lang
    _base_url: URL

    _client: Client | None = None
    _lang_data: dict[str, str] | None = None

    def __init__(self, base_url: str | None = None, lang: Lang | None = None):
        self._base_url = URL(
            base_url
            or "https://git.neeemooo.com/githubbackup/GenshinData/-/raw/master/"
        )
        self._lang = lang or "chs"

    @property
    def lang(self) -> Lang:
        return self._lang

    @property
    def client(self) -> Client:
        with self._lock:
            if self._client is None or self._client.is_closed:
                self._client = Client(verify=ssl_context)
        return self._client

    def refresh(self) -> None:
        """删除缓存数据的文件夹，需要数据时会重新从网络上下载，达到刷新缓存数据的目的"""
        if self._client is not None:
            if not self._client.is_closed:
                self._client.close()
            self._client = None
        if DATA_DIR.exists():
            os.remove(DATA_DIR)
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    @lru_cache(128, typed=True)
    def get_text(self, text_id: int | str | None) -> str | None:
        if text_id is None:
            return None
        if self._lang_data is None:
            self._lang_data = self.fetch("TextMap" + self.lang.upper(), "TextMap")
        result = self._lang_data.get(str(text_id), None)
        if result is not None:
            return result.replace("\\n", "\n")
        return result

    @lru_cache()
    def fetch(self, name: str, file_dir: str = "ExcelBinOutput") -> Json:
        file_path = DATA_DIR.joinpath(file_dir).joinpath(name).with_suffix(".json")
        file_path.parent.mkdir(exist_ok=True, parents=True)

        if not file_path.exists() or os.stat(file_path) == 0:
            response = self.client.get(str(self._base_url / file_dir / file_path.name))
            response.raise_for_status()
            with open(file_path, encoding="utf-8", mode="w") as file:
                file.write(content := response.text)
                return json.loads(content)

        with open(file_path, encoding="utf-8", mode="r") as file:
            return json.loads(file.read())
