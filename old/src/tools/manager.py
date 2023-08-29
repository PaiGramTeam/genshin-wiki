import ujson as json
import ssl
from functools import lru_cache
import os

from pydantic import Json
from yarl import URL
from httpx import AsyncClient as Client

from utils.const import DATA_DIR
from utils.typedefs import Lang

ssl_context = ssl.SSLContext()


class ResourceManager:
    _lang: Lang
    _base_url: URL

    _client: Client | None = None
    _lang_data: dict[str, str] | None = None

    def __init__(self, lang: Lang | None = None, *, base_url: str | None = None):
        self._base_url = URL(
            base_url or "https://gitlab.com/Dimbreath/AnimeGameData/-/raw/master/"
        )
        self._lang = lang or os.environ.get("LANG", None) or "chs"

    @property
    def lang(self) -> Lang:
        return self._lang

    @property
    def client(self) -> Client:
        from httpx import Timeout

        if self._client is None or self._client.is_closed:
            self._client = Client(verify=ssl_context, timeout=Timeout(timeout=30))
        return self._client

    # @lru_cache()
    async def fetch(self, name: str, file_dir: str = "ExcelBinOutput") -> Json:
        file_path = DATA_DIR.joinpath(file_dir).joinpath(name).with_suffix(".json")
        file_path.parent.mkdir(exist_ok=True, parents=True)

        if not (file_path.exists() and os.stat(file_path)):
            response = await self.client.get(
                str(self._base_url / file_dir / file_path.name)
            )
            response.raise_for_status()
            with open(file_path, encoding="utf-8", mode="w") as file:
                file.write(content := response.text)
                return json.loads(content)

        with open(file_path, encoding="utf-8", mode="r") as file:
            return json.loads(file.read())

    @lru_cache(256, typed=True)
    async def __call__(self, text_id: int | str | None) -> str | None:
        if text_id is None:
            return None
        if self._lang_data is None:
            self._lang_data = await self.fetch("TextMap" + self.lang.upper(), "TextMap")
        result = self._lang_data.get(str(text_id), None)
        if result is not None:
            return result.replace("\\n", "\n")
        return result
