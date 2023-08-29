from ormar import Float, ForeignKey, Integer, JSON, ManyToMany, String, Text
from pydantic import Json

from models._base import Model, ModelMeta
from models.other import ItemCount

__all__ = (
    "Talent",
    "NormalAttack",
    "ElementalBurst",
    "ElementalSkill",
    "AlternateSprint",
    "PassiveTalent",
    "AscensionPassive",
    "FirstAscensionPassive",
    "FourthAscensionPassive",
    "UtilityPassive",
    "MiscellaneousPassive",
    "AvatarTalents",
    "TalentAttribute",
)


class Talent(Model):
    class Meta(ModelMeta):
        abstract = True

    id: int = Integer(primary_key=True)
    """ID"""
    name: str = String(max_length=255)
    """天赋名称"""
    description: str = Text()
    """天赋描述"""
    icon: str = String(max_length=255)
    """天赋图标名"""
    promote_level: int = Integer(default=0)
    """解锁等级"""


class TalentAttribute(Model):
    class Meta(ModelMeta):
        tablename = "avatar_talent_attribute"

    id: int = Integer(primary_key=True)
    """ID"""
    level: int = Integer(default=1)
    """等级"""
    params: Json[list[float]] = JSON(default=[])
    """参数数值"""
    break_level: int = Integer(default=0)
    """突破所需等级"""
    coin: int = Integer(default=0)
    """摩拉"""
    cost_items: list[ItemCount] = ManyToMany(ItemCount)
    """消耗物品"""


class CombatTalent(Model):
    """战斗天赋"""

    class Meta:
        abstract = True

    id: int = Integer(primary_key=True)

    cooldown: float = Float()
    """冷却时间"""
    param_descriptions: Json[list[str]] = JSON(default=[])
    """参数描述"""


class NormalAttack(CombatTalent):
    """普通攻击"""

    class Meta(ModelMeta):
        tablename = "avatar_talent_normal_attack"

    attributes: list[TalentAttribute] = ManyToMany(TalentAttribute)
    """数值参数"""

class ElementalSkill(CombatTalent):
    """元素战技"""

    class Meta(ModelMeta):
        tablename = "avatar_talent_elemental_skill"

    attributes: list[TalentAttribute] = ManyToMany(TalentAttribute)
    """数值参数"""

class ElementalBurst(CombatTalent):
    """元素爆发"""

    class Meta(ModelMeta):
        tablename = "avatar_talent_elemental_burst"

    attributes: list[TalentAttribute] = ManyToMany(TalentAttribute)
    """数值参数"""

class AlternateSprint(CombatTalent):
    """冲刺技能"""

    class Meta(ModelMeta):
        tablename = "avatar_talent_alternate_sprint"

    attributes: list[TalentAttribute] = ManyToMany(TalentAttribute)
    """数值参数"""

class PassiveTalent(Talent):
    """固有天赋"""

    class Meta(ModelMeta):
        abstract = True

    attribute: TalentAttribute = ForeignKey(TalentAttribute)
    """数值参数"""


class AscensionPassive(PassiveTalent):
    """突破固有天赋"""

    class Meta(ModelMeta):
        abstract = True

    ascension: int
    """突破次数"""


class FirstAscensionPassive(AscensionPassive):
    """第一次突破固有天赋"""

    class Meta(ModelMeta):
        tablename = "avatar_talent_first_ascension_passive"

    ascension = 1


class FourthAscensionPassive(AscensionPassive):
    """第四次突破固有天赋"""

    class Meta(ModelMeta):
        tablename = "avatar_talent_fourth_ascension_passive"

    ascension = 4


class UtilityPassive(PassiveTalent):
    """实用固有天赋"""

    class Meta(ModelMeta):
        tablename = "avatar_talent_utility_passive"


class MiscellaneousPassive(PassiveTalent):
    """杂项固有天赋"""

    class Meta(ModelMeta):
        tablename = "avatar_talent_miscellaneous_passive"


class AvatarTalents(Model):
    """角色天赋"""

    class Meta(ModelMeta):
        tablename = "avatar_talents"

    id: int = Integer(primary_key=True)

    normal_attack: NormalAttack = ForeignKey(NormalAttack)
    """普通攻击"""
    elemental_skill: ElementalSkill | None = ForeignKey(ElementalSkill, nullable=True)
    """元素战技"""
    elemental_burst: ElementalBurst | None = ForeignKey(ElementalBurst, nullable=True)
    """元素爆发"""
    alternate_sprint: AlternateSprint | None = ForeignKey(
        AlternateSprint, nullable=True
    )
    """冲刺技能"""

    first_ascension_passive: FirstAscensionPassive | None = ForeignKey(
        FirstAscensionPassive, nullable=True
    )
    """第一次突破固有天赋"""

    fourth_ascension_passive: FourthAscensionPassive | None = ForeignKey(
        FourthAscensionPassive, nullable=True
    )
    """第四次突破固有天赋"""
    utility_passive: UtilityPassive | None = ForeignKey(UtilityPassive, nullable=True)
    """实用固有天赋"""
    miscellaneous_passive: MiscellaneousPassive | None = ForeignKey(
        MiscellaneousPassive, nullable=True
    )
    """杂项固有天赋"""

ModelMeta.metadata.create_all()