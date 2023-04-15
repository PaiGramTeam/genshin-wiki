from typing import TYPE_CHECKING

from models.enums import AvatarQuality, WeaponType
from utils.model import BaseModel

if TYPE_CHECKING:
    from models.item import Item


class AvatarBirth(BaseModel):
    month: int
    """月"""
    day: int
    """日"""


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

    cn_cv: str
    jp_cv: str
    en_cv: str
    kr_cv: str


class AvatarItem(BaseModel):
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
    items: list[AvatarItem]
    """突破所需材料"""


class Avatar(BaseModel):
    id: int
    """角色ID"""
    name: str
    """名称"""
    quality: AvatarQuality
    """品质"""
    weapon: WeaponType
    """武器类型"""
    information: AvatarInfo
    """角色信息"""
    promote: AvatarPromote
    """角色突破数据"""
