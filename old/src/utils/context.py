from contextlib import contextmanager
from contextvars import ContextVar, Token
from typing import TypeVar

from utils.single import Singleton

__all__ = ("ContextManager",)

T = TypeVar("T")

_values: dict[str, ContextVar] = {}


class ContextManager(Singleton):
    _values: dict[str, ContextVar] = {}

    def get_context(self, name: str) -> ContextVar[T]:
        if name in self._values:
            return self._values[name]
        else:
            result = ContextVar(name)
            self._values[name] = result
            return result

    def get_value(self, name: str) -> T:
        return self.get_context(name).get()

    def set_context(self, name: str, value: T) -> Token:
        context: ContextVar[T] = self.get_context(name)
        return context.set(value)

    def reset_context(self, name: str, token: Token) -> None:
        context: ContextVar[T] = self.get_context(name)
        context.reset(token)

    @contextmanager
    def with_context(self, name: str, value: T) -> T:
        context: ContextVar[T] = self.get_context(name)
        token: Token = context.set(value)
        try:
            yield value
        finally:
            context.reset(token)

    def __getitem__(self, item: str) -> ContextVar[T]:
        return self.get_context(item)
