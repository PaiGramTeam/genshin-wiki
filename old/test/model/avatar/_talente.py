from typing import ClassVar

from model.other import ItemCount
from utils.model import BaseModel

__all__ = (
    "Talent",
    "CombatTalent",
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


class Talent(BaseModel):
    name: str
    """天赋名称"""
    description: str
    """天赋描述"""
    icon: str
    """图标"""
    promote_level: int = 0
    """解锁等级"""


class TalentAttribute(BaseModel):
    level: int = 1
    """等级"""
    params: list[float] = []
    """参数数值"""

    break_level: int = 0
    """所需突破等级"""
    coin: int = 0
    """摩拉"""
    cost_items: list[ItemCount] = []
    """消耗物品"""


class CombatTalent(Talent):
    """战斗天赋"""

    cooldown: float = 0
    """冷却时间"""
    param_descriptions: list[str] = []
    """参数描述"""
    attributes: list[TalentAttribute]
    """数值参数"""


class NormalAttack(CombatTalent):
    """普通攻击"""


class ElementalSkill(CombatTalent):
    """元素战技"""


class ElementalBurst(CombatTalent):
    """元素爆发"""


class AlternateSprint(CombatTalent):
    """冲刺技能"""


class PassiveTalent(Talent):
    """固有天赋"""

    attribute: TalentAttribute
    """数值参数"""


class AscensionPassive(PassiveTalent):
    """突破固有天赋"""

    ascension: ClassVar[int]


class FirstAscensionPassive(AscensionPassive):
    """第一次突破固有天赋"""

    ascension = 1


class FourthAscensionPassive(AscensionPassive):
    """第四次突破固有天赋"""

    ascension = 4


class UtilityPassive(PassiveTalent):
    """实用固有天赋"""


class MiscellaneousPassive(PassiveTalent):
    """杂项固有天赋"""


class AvatarTalents(BaseModel):
    """角色天赋"""

    normal_attack: NormalAttack
    """普通攻击"""
    elemental_skill: ElementalSkill | None
    """元素战技"""
    elemental_burst: ElementalBurst | None
    """元素爆发"""
    alternate_sprint: AlternateSprint | None = None
    """冲刺技能"""

    first_ascension_passive: FirstAscensionPassive | None
    """第一次突破固有天赋"""
    fourth_ascension_passive: FourthAscensionPassive | None
    """第四次突破固有天赋"""
    utility_passive: UtilityPassive | None = None
    """实用固有天赋"""
    miscellaneous_passive: MiscellaneousPassive | None = None
    """杂项固有天赋"""
