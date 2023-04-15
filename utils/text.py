from utils.context import ContextManager

__all__ = ("Text",)


class Text(str):
    def __new__(cls, string: str | int) -> "Text":
        _id = None
        if isinstance(string, str):
            try:
                _id = int(string)
            except ValueError:
                _id = None
        elif isinstance(string, int):
            _id = string
        if _id is not None:
            string = (
                ContextManager().get_value("resource_manager").get_text(_id) or ""
            ).replace("\\n", "\n")
        return str.__new__(cls, string)
