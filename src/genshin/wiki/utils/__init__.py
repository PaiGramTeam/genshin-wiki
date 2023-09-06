from collections import OrderedDict
from typing import TypeVar

__all__ = ("LimitedSizeDict", )

K = TypeVar('K')
V = TypeVar('V')


class LimitedSizeDict(OrderedDict[K, V]):
    def __init__(self, *args, size_limit: int | None = None, **kwargs) -> None:
        self.size_limit = size_limit
        OrderedDict.__init__(self, *args, **kwargs)
        self._check_size_limit()

    def __setitem__(self, key: K, value: V) -> None:
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self) -> None:
        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=False)