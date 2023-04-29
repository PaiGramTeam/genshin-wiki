import asyncio
from abc import ABC, abstractmethod
from asyncio import Task

targets: list["Target"] = []


class Target(ABC):
    _task: Task | None = None

    @property
    def task(self) -> Task:
        return self._task

    def __init__(self):
        targets.append(self)

    async def __async_init__(self) -> None:
        pass

    async def __async_del__(self) -> None:
        pass

    @abstractmethod
    async def run(self) -> None:
        pass

    async def _run(self) -> None:
        await self.__async_init__()
        await self.run()
        await self.__async_del__()

    async def run_in_background(self) -> Task:
        self._task = asyncio.create_task(self._run())
        return self._task


async def waiting_for_done():
    task_list: list[Task] = []
    for target in targets:
        if target.task is not None and not target.task.done():
            task_list.append(target.task)

    await asyncio.gather(*task_list)
