try:
    import regex as re
except ImportError:
    import re

__all__ = ("remove_rich_tag",)


def remove_rich_tag(string: str | None) -> str:
    """去除富文本标签"""
    if string is not None:
        return re.sub(
            r"(<(?P<tag_name>[a-z]+?)=(?P<value>.+?)>.+?</(?P=tag_name)>)", "", string
        )
