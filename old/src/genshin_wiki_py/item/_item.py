from ormar import Integer, JSON, UniqueColumns, property_field
from pydantic import Json, PrivateAttr

from genshin_wiki._model import ForeignKey, MapString, MapText, Model, ModelMeta
from genshin_wiki.manager import resource_manager


class ItemDescription(Model):
    class Meta(ModelMeta):
        tablename = "item_description"
        constraints = [UniqueColumns("main", "codex", "special")]

    id: int = Integer(primary_key=True)
    """ID"""
    main: str | None = MapText(nullable=True)
    """描述"""
    codex: str | None = MapText(nullable=True)
    """图鉴描述"""
    special: str | None = MapText(nullable=True)
    """特殊描述"""


class Item(Model):
    class Meta(ModelMeta):
        tablename = "item"
        constraints = [UniqueColumns("name", "type")]

    id: int = Integer(primary_key=True)
    """ID"""
    name: str = MapString()
    """名称"""
    type: str = MapString()
    """类型"""
    rarity: int | None = Integer(minimum=0, maximum=5, default=None, nullable=True)
    """稀有度"""
    _source: Json[list] | None = PrivateAttr(JSON(nullable=True, name="source", default=None))
    """来源"""
    description: ItemDescription = ForeignKey(ItemDescription)
    """描述"""

    @property_field
    def source(self) -> Json[list[str]] | None:
        if self._source is None:
            return self._source
        return list(
            filter(
                lambda x: x, map(lambda x: resource_manager.get_text(x), self._source)
            )
        )


ModelMeta.metadata.create_all()
