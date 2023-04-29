from utils.model import BaseModel
from typing import ClassVar

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
)


class Talent(BaseModel):
    name: str
    """天赋名称"""
    description: str
    """天赋描述"""
    icon: str
    """图标"""
    level: int = 0
    """解锁等级"""

    params: list[float] = []
    """数值参数列表"""


class CombatTalent(Talent):
    """战斗天赋"""

    cooldown: float = 0
    """冷却时间"""


class NormalAttack(CombatTalent):
    """普通攻击"""


class ElementalSkill(CombatTalent):
    """元素战技"""


class ElementalBurst(CombatTalent):
    """元素爆发"""


class AlternateSprint(CombatTalent):
    """冲刺技能"""


class PassiveTalent(Talent):
    """被动天赋"""


class AscensionPassive(PassiveTalent):
    """突破被动天赋"""

    ascension: ClassVar[int]


class FirstAscensionPassive(AscensionPassive):
    """第一次突破被动天赋"""

    ascension = 1


class FourthAscensionPassive(AscensionPassive):
    """第四次突破被动天赋"""

    ascension = 4


class UtilityPassive(PassiveTalent):
    """实用被动天赋"""


class MiscellaneousPassive(PassiveTalent):
    """杂项被动天赋"""


class AvatarTalents(BaseModel):
    """角色天赋"""

    normal_attack: NormalAttack
    """普通攻击"""
    elemental_skill: ElementalSkill
    """元素战技"""
    elemental_burst: ElementalBurst
    """元素爆发"""
    alternate_sprint: AlternateSprint | None = None
    """冲刺技能"""

    first_ascension_passive: FirstAscensionPassive
    fourth_ascension_passive: FourthAscensionPassive
    utility_passive: UtilityPassive | None = None
    miscellaneous_passive: MiscellaneousPassive | None = None
