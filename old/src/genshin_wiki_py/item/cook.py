from ormar import Integer, property_field

from genshin_wiki._model import Model, ModelMeta, String, Enum, ForeignKey
from genshin_wiki.enums import FoodQuality
from genshin_wiki.item._item import Item


class Food(Model):
    class Meta(ModelMeta):
        tablename = "food"

    id: int = Integer(primary_key=True)
    """ID"""
    _item: Item = ForeignKey(Item, name="item", nullable=False)
    """相关物品"""

    @property_field
    def name(self) -> str:
        return self._item.name

    @property_field
    def type(self) -> str:
        return self._item.type

    @property_field
    def rarity(self) -> int:
        return self._item.rarity or 0

    effect: str | None = String(nullable=True)
    """效果"""

    @property_field
    def source(self) -> list[str]:
        return self._item._source or []

    @property_field
    def description(self) -> str | None:
        return self._item.description

    @property_field
    def description_codex(self) -> str | None:
        return self._item.description_codex


ModelMeta.metadata.create_all()
