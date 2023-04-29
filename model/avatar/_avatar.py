from typing import TYPE_CHECKING

from model.enums import AvatarQuality, Element, WeaponType
from utils.model import BaseModel

if TYPE_CHECKING:
    from model.item import Item

__all__ = (
    "Avatar",
    "AvatarBirth",
    "AvatarInfo",
    "AvatarConstellation",
    "AvatarPromote",
    "Seuyu",
    "ItemCount",
)


class AvatarBirth(BaseModel):
    """角色生日"""

    month: int
    """月"""
    day: int
    """日"""


class Seuyu(BaseModel):
    """声优"""

    cn: str
    """汉语CV"""
    jp: str
    """日语CV"""
    en: str
    """英语CV"""
    kr: str
    """韩语CV"""


class AvatarInfo(BaseModel):
    title: str
    """称号"""
    birth: AvatarBirth
    """生日"""
    occupation: str
    """所属"""
    vision: str
    """神之眼"""
    constellation: str
    """星座"""
    description: str
    """描述"""
    seuyu: Seuyu
    """声优"""


class ItemCount(BaseModel):
    item: "Item"
    """物品"""
    count: int
    """数量"""


class AvatarPromote(BaseModel):
    required_level: int = 0
    """突破所需等级"""
    promote_level: int = 0
    """突破等级"""
    max_level: int
    """解锁的等级上限"""

    coin: int = 0
    """摩拉"""
    items: list[ItemCount] = []
    """突破所需材料"""


class AvatarConstellation(BaseModel):
    """角色命座"""

    name: str
    """命座名"""
    description: str
    """命座描述"""
    icon: str
    """命座图标"""


class Avatar(BaseModel):
    """角色"""

    id: int
    """角色ID"""
    name: str
    """名称"""
    element: Element
    """元素"""
    quality: AvatarQuality
    """品质"""
    weapon_type: WeaponType
    """武器类型"""
    information: AvatarInfo
    """角色信息"""
    promote: AvatarPromote
    """角色突破数据"""
    constellations: list[AvatarConstellation]
    """角色命座信息"""
