from ormar import Boolean, Integer, JSON, Text, ForeignKey
from pydantic import Json

from models._base import Enum, Model, ModelMeta, String
from models.enums import FoodQuality


class Item(Model):
    class Meta(ModelMeta):
        tablename = 'item_simple'
    id: int = Integer(primary_key=True)
    """ID"""
    name: str = String()
    """名称"""
    type: str = String()
    """类型"""
    rarity: int | None = Integer(minimum=0, maximum=5, default=None, nullable=True)
    """稀有度"""
    description: str | None = Text()
    """描述"""
    description_codex: str | None = Text(nullable=True)
    """图鉴描述"""

class OldItem(Model):
    class Meta(ModelMeta):
        tablename = "item"

    id: int = Integer(primary_key=True)
    """ID"""
    name: str = String()
    """名称"""
    type: str | None = String(nullable=True)
    """类型"""
    icon: str = String()
    """图标名"""
    rarity: int | None = Integer(minimum=0, maximum=5, default=None, nullable=True)
    """稀有度"""
    description: str | None = Text(nullable=True)
    """描述"""
    special_description: str | None = Text(nullable=True)
    """特殊描述"""
    is_virtual: bool = Boolean()
    """是否为虚拟物品"""
    ########################################
    ################# Food #################
    ########################################
    quality: FoodQuality | None = Enum(FoodQuality, nullable=True, default=None)
    """食物质量"""
    effect: str | None = Text(nullable=True, default=None)
    """效果"""
    effect_icon: str | None = String(nullable=True, default=None)
    """效果图标"""
    cd_time: int | None = Integer(nullable=True, default=None)
    """效果持续时间"""
    cd_group: int | None = Integer(nullable=True, default=None)
    """效果CD组"""
    ########################################
    ############### Material ###############
    ########################################
    material_type: str | None = String(nullable=True, default=None)
    """材料类型"""
    material_type_description: str | None = Text(nullable=True, default=None)
    """材料类型描述"""
    ########################################
    ############### Namecard ###############
    ########################################
    pictures: Json[list[str]] | None = JSON(default=None, nullable=True)
    """名片对应图标名"""
    ########################################
    ############### Other ##################
    ########################################
    close_bag_after_used: bool | None = Boolean(nullable=True, default=None)
    """使用后是否关闭背包"""
    interaction_title: str | None = String(nullable=True, default=None)
    """交互标题"""
    is_force_get_hint: bool | None = Boolean(nullable=True, default=None)
    """是否强制获取提示"""
    no_first_get_hint: bool | None = Boolean(nullable=True, default=None)
    """是否没有第一次获取提示"""
    use_on_gain: bool | None = Boolean(nullable=True, default=None)
    """在获取时使用"""
    use_target: str | None = String(nullable=True, default=None)
    """使用目标"""


ModelMeta.metadata.create_all()
