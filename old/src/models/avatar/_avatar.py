from ormar import Float, ForeignKey, Integer, JSON, ManyToMany, Text
from pydantic import Json

from models._base import Enum, Model, ModelMeta, String
from models.avatar.talente import AvatarTalents
from models.enums import Association, AvatarQuality, Element, PropType, WeaponType
from models.item import OldItem
from models.other import ItemCount


class AvatarIcon(Model):
    """角色图标"""

    class Meta(ModelMeta):
        tablename = "avatar_icon"

    id: int = Integer(primary_key=True)
    """ID"""
    icon_name: str = String()
    """图标名"""
    side_icon_name: str = String()
    """侧视图图标名"""


class AvatarBirthday(Model):
    """角色生日"""

    class Meta(ModelMeta):
        tablename = "avatar_birthday"

    id: int = Integer(primary_key=True)

    month: int = Integer(minimum=1, maximum=12)
    day: int = Integer(minimum=1, maximum=31)


class AvatarSeuyu(Model):
    """角色声优"""

    class Meta(ModelMeta):
        tablename = "avatar_seuyu"

    id: int = Integer(primary_key=True)

    chinese: str = String()
    japanese: str = String()
    english: str = String()
    korean: str = String()


class AvatarStory(Model):
    """角色故事（单个）"""

    class Meta(ModelMeta):
        tablename = "avatar_story"

    id: int = Integer(primary_key=True)
    title: str = String()
    content: str = Text()
    tips: Json[list[str]] = JSON()


class AvatarStories(Model):
    """角色故事"""

    class Meta(ModelMeta):
        tablename = "avatar_story_list"

    id: int = Integer(primary_key=True)
    details: AvatarStory = ForeignKey(AvatarStory, skip_reverse=True, related_name='avatar_stories_details')
    story_1: AvatarStory = ForeignKey(AvatarStory, skip_reverse=True, related_name='avatar_stories_story_1')
    story_2: AvatarStory = ForeignKey(AvatarStory, skip_reverse=True, related_name='avatar_stories_story_2')
    story_3: AvatarStory = ForeignKey(AvatarStory, skip_reverse=True, related_name='avatar_stories_story_3')
    story_4: AvatarStory = ForeignKey(AvatarStory, skip_reverse=True, related_name='avatar_stories_story_4')
    story_5: AvatarStory = ForeignKey(AvatarStory, skip_reverse=True, related_name='avatar_stories_story_5')
    miscellaneous: AvatarStory | None = ForeignKey(
        AvatarStory, nullable=True, skip_reverse=True, default=None, related_name='avatar_stories_miscellaneous'
    )
    vision: AvatarStory | None = ForeignKey(
        AvatarStory, nullable=True, skip_reverse=True, default=None, related_name='avatar_stories_vision'
    )


class AvatarInfo(Model):
    class Meta(ModelMeta):
        tablename = "avatar_info"

    id: int = Integer(primary_key=True)
    title: str | None = String(nullable=True)
    """称号"""
    birthday: AvatarBirthday | None = ForeignKey(AvatarBirthday, skip_reverse=True)
    """称号"""
    occupation: str = String()
    """所属"""
    vision: str = String()
    """神之眼"""
    special_food: OldItem | None = ForeignKey(OldItem, skip_reverse=True, nullable=True)
    """特殊料理"""
    constellation: str = String()
    """星座"""
    description: str = Text()
    """描述"""
    association: Association = Enum(Association)
    """联系"""
    seuyu: AvatarSeuyu = ForeignKey(AvatarSeuyu, skip_reverse=True)
    """声优"""
    stories: AvatarStories = ForeignKey(AvatarStories, skip_reverse=True)
    """故事"""


class AvatarAttribute(Model):
    """角色属性"""

    class Meta(ModelMeta):
        tablename = "avatar_attribute"

    id: int = Integer(primary_key=True)

    HealthPoints: float = Float()
    """生命值"""
    Attack: float = Float()
    """攻击力"""
    Defense: float = Float()
    """防御力"""
    CriticalRate: float = Float()
    """暴击率"""
    CriticalHurtRate: float = Float()
    """暴击伤害"""
    ChargeEfficiency: float = Float()
    """元素充能效率"""


class AddProp(Model):
    """属性加成"""

    class Meta(ModelMeta):
        tablename = "avatar_add_prop"

    id: int = Integer(primary_key=True)

    type: PropType = Enum(PropType)
    """属性类型"""
    value: float = Float()
    """属性值"""


class AvatarPromote(Model):
    """角色突破数据"""

    class Meta(ModelMeta):
        tablename = "avatar_promote"

    id: int = Integer(primary_key=True)

    promote_level: int = Integer(default=0)
    """突破等级"""
    max_level: int = Integer()
    """解锁的等级上限"""
    add_props: list[AddProp] | None = ManyToMany(AddProp)
    """属性加成"""

    coin: int = Integer(default=0)
    """消耗摩拉"""
    cost_item: list[ItemCount] | None = ManyToMany(ItemCount)
    """突破所需材料"""

class AvatarConstellation(Model):
    """角色命座信息"""
    class Meta(ModelMeta):
        tablename = "avatar_constellation"

    id: int = Integer(primary_key=True)

    name: str = String()
    """命座名"""
    description: str = Text()
    """描述"""
    icon: str = String()
    """命座图标"""
    param_list: Json[list[float]] = JSON()
    """命座数据参数列表"""

class Avatar(Model):
    """角色"""

    class Meta(ModelMeta):
        tablename = "avatar"

    id: int = Integer(primary_key=True)
    """ID"""
    name: str = String()
    """名称"""
    icon: AvatarIcon = ForeignKey(AvatarIcon, skip_reverse=True)
    """图标"""
    element: Element = Enum(Element)
    """元素"""
    quality: AvatarQuality = Enum(AvatarQuality)
    """品质"""
    weapon_type: WeaponType = Enum(WeaponType)
    """武器类型"""
    information: AvatarInfo = ForeignKey(AvatarInfo, skip_reverse=True)
    """角色信息"""
    attributes: AvatarAttribute = ForeignKey(AvatarAttribute)
    """角色基础属性"""
    talents: AvatarTalents = ForeignKey(AvatarTalents, skip_reverse=True)
    """角色天赋信息"""
    promotes: list[AvatarPromote] = ManyToMany(AvatarPromote)
    """角色突破数据"""
    constellations: list[AvatarConstellation] = ManyToMany(AvatarConstellation)
    """角色命座信息"""

ModelMeta.metadata.create_all()