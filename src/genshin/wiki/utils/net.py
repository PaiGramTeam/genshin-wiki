from multiprocessing import Lock
from typing import TYPE_CHECKING

from aiohttp import ClientResponse, ClientSession

if TYPE_CHECKING:
    from multiprocessing.synchronize import Lock as LockType


class Net:
    _lock: "LockType" = Lock()

    _session: ClientSession | None = None

    @property
    def session(self) -> ClientSession:
        with self._lock:
            if self._session is None:
                self._session = ClientSession()
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._session and not self._session.closed:
            # noinspection PyBroadException
            try:
                import asyncio

                asyncio.run(self._session.close())
            except:
                pass

    async def _request(self, *args, **kwargs) -> ClientResponse:
        time = 0
        while True:
            try:
                return await self.session.request(*args, **kwargs)
            except Exception as e:
                if time > 3:
                    raise e
                time += 1

    async def _get(self, *args, **kwargs) -> ClientResponse:
        return await self._request("GET", *args, **kwargs)