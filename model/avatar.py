from typing import TYPE_CHECKING

from model.enums import AvatarQuality, Element, WeaponType
from utils.model import BaseModel

if TYPE_CHECKING:
    from model.item import Item


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


class AvatarSkill(BaseModel):
    name: str
    """技能名称"""
    description: str
    """技能描述"""
    promote_level: int = 0
    """所需突破等级"""
    icon: str
    """图标"""


class AvatarActiveSkill(AvatarSkill):
    """角色主动技能"""

    CD: float
    """冷却时间"""
    max_charge_num: int
    """技能最大储存次数"""


class AvatarPassiveSkill(AvatarSkill):
    """角色被动技能"""


class AvatarSkills(BaseModel):
    attack_skill: AvatarActiveSkill
    """普通攻击"""
    energy_skill: AvatarActiveSkill
    """元素爆发"""
    proud_skills: list[AvatarSkill]
    """被动技能"""


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
