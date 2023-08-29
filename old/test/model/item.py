from model.enums import FoodQuality, ItemType
from utils.model import BaseModel


class Item(BaseModel):
    id: int
    """ID"""
    name: str
    """名称"""
    type: str | None
    """类型"""
    icon: str
    """图标名"""
    rarity: int | None
    """星级"""
    description: str
    """描述"""
    special_description: str | None
    """特殊描述"""
    item_type: ItemType
    """物品类型"""


class Material(Item):
    material_type: str
    """材料类型"""
    material_type_description: str
    """材料类型描述"""


class Food(Item):
    quality: FoodQuality | None
    """食物质量"""
    effect: str
    """效果"""
    effect_icon: str
    """效果图标"""
    # effect_name: str
    # """效果名称"""


class Namecard(Item):
    pictures: list[str]
    """其它图标名"""
