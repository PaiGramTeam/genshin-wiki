from model.avatar._talente import AvatarTalents
from model.enums import Association, AvatarQuality, Element, WeaponType
from model.other import ItemCount
from utils.model import BaseModel

__all__ = (
    "Avatar",
    "AvatarBirth",
    "AvatarInfo",
    "AvatarConstellation",
    "AvatarPromote",
    "AvatarStories",
    "Story",
    "Seuyu",
    "AvatarAttribute",
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

    miscellaneous: Story | None = None
    """角色杂谈"""

    vision: Story | None = None
    """神之眼"""


class AvatarInfo(BaseModel):
    title: str | None
    """称号"""
    birth: AvatarBirth | None
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


class AvatarPromote(BaseModel):
    promote_level: int = 0
    """突破等级"""
    max_level: int
    """解锁的等级上限"""

    coin: int = 0
    """摩拉"""
    cost_items: list[ItemCount] = []
    """突破所需材料"""


class AvatarConstellation(BaseModel):
    """角色命座"""

    name: str
    """命座名"""
    description: str
    """命座描述"""
    icon: str
    """命座图标"""
    param_list: list[float]
    """命座数据参数列表"""


class AvatarAttribute(BaseModel):
    """角色属性"""

    HP: float
    """生命值"""
    Attack: float
    """攻击力"""
    Defense: float
    """防御力"""
    Critical: float
    """暴击率"""
    CriticalDamage: float
    """暴击伤害"""
    ChargeEfficiency: float
    """元素充能效率"""
    ElementalMastery: float = 0
    """元素精通"""
    PhysicalAddHurt: float = 0
    """物理伤害加成"""
    PyroAddHurt: float = 0
    """火元素伤害加成"""
    HydroAddHurt: float = 0
    """水元素伤害加成"""
    AnemoAddHurt: float = 0
    """风元素伤害加成"""
    ElectroAddHurt: float = 0
    """雷元素伤害加成"""
    DendroAddHurt: float = 0
    """草元素伤害加成"""
    CryoAddHurt: float = 0
    """冰元素伤害加成"""
    GeoAddHurt: float = 0
    """岩元素伤害加成"""


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
    attributes: AvatarAttribute
    """角色基础属性"""
    talents: AvatarTalents
    """角色天赋信息"""
    promotes: list[AvatarPromote]
    """角色突破数据"""
    constellations: list[AvatarConstellation]
    """角色命座信息"""
