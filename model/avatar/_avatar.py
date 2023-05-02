from typing import TYPE_CHECKING

from model.enums import Association, AvatarQuality, Element, WeaponType
from utils.model import BaseModel

if TYPE_CHECKING:
    from model.item import Item
    from model.avatar._talente import AvatarTalents

__all__ = (
    "Avatar",
    "AvatarBirth",
    "AvatarInfo",
    "AvatarConstellation",
    "AvatarPromote",
    "AvatarStories",
    "Story",
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


class Story(BaseModel):
    """故事"""

    title: str
    """标题"""
    content: str
    """内容"""
    tips: list[str]
    """提示"""


class AvatarStories(BaseModel):
    """角色故事"""

    details: Story
    """角色详情"""

    story_1: Story
    """角色故事1"""

    story_2: Story
    """角色故事2"""

    story_3: Story
    """角色故事3"""

    story_4: Story
    """角色故事4"""

    story_5: Story
    """角色故事5"""

    miscellaneous: Story
    """角色杂谈"""

    vision: Story
    """神之眼"""


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
    association: Association
    """区域"""
    seuyu: Seuyu
    """声优"""
    stories: AvatarStories
    """故事"""


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
    talents: "AvatarTalents"
    """角色天赋信息"""
    constellations: list[AvatarConstellation]
    """角色命座信息"""
