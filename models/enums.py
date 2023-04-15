from enum import StrEnum


class AvatarQuality(StrEnum):
    Orange = "ORANGE"
    """五星"""
    Purple = "PURPLE"
    """四星"""
    Special = "SPECIAL"
    """特殊"""


class WeaponType(StrEnum):
    Sword = "SWORD"
    """单手剑"""
    Claymore = "CLAYMORE"
    """双手剑"""
    Bow = "BOW"
    """弓"""
    Catalyst = "CATALYST"
    """法器"""
    Polearm = "POLEARM"
    """长柄武器"""


class Element(StrEnum):
    Pyro = "PYRO"
    """火"""
    Hydro = "HYDRO"
    """水"""
    Anemo = "ANEMO"
    """风"""
    Electro = "ELECTRO"
    """雷"""
    Dendro = "DENDRO"
    """草"""
    Cryo = "CRYO"
    """冰"""
    Geo = "GEO"
    """岩"""
    Null = "NULL"
    """无"""


class PropType(StrEnum):
    HP = "HP"
    """生命值"""
    HP_P = "HPPercent"
    """生命值百分比"""

    Defense = "Defense"
    """防御力"""
    Defense_P = "DefensePercent"
    """防御力百分比"""

    Attack = "Attack"
    """攻击力"""
    Attack_P = "AttackPercent"
    """攻击力百分比"""

    Critical = "Critical"
    """暴击率"""
    CriticalHurt = "CriticalHurt"
    """暴击伤害"""

    Heal = "HealAdd"
    """治疗加成"""
    Element = "ElementMastery"
    """元素精通"""
    Charge = "ChargeEfficiency"
    """元素充能效率"""

    Physical = "PhysicalAddHurt"
    """物理伤害加成"""
    Pyro = "PyroAddHurt"
    """火元素伤害加成"""
    Hydro = "HydroAddHurt"
    """水元素伤害加成"""
    Anemo = "AnemoAddHurt"
    """风元素伤害加成"""
    Electro = "ElectroAddHurt"
    """雷元素伤害加成"""
    Dendro = "DendroAddHurt"
    """草元素伤害加成"""
    Cryo = "CryoAddHurt"
    """冰元素伤害加成"""
    Geo = "GeoAddHurt"
    """岩元素伤害加成"""
