from ormar import ForeignKey, Integer, Text

from models._base import Enum, Model, ModelMeta, String
from models.enums import FoodQuality
from models.item._item import OldItem


class Food(Model):
    """食物"""

    class Meta(ModelMeta):
        tablename = "item_food"

    id: int = Integer(primary_key=True)
    item: OldItem = ForeignKey(OldItem)
    """相关物品"""
    quality: FoodQuality | None = Enum(FoodQuality, nullable=True)
    """食物质量"""
    effect: str | None = Text(nullable=True)
    """效果"""
    effect_icon: str = String()
    """效果图标"""
