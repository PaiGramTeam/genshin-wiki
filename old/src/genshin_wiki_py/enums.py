from enum import StrEnum


class AvatarQuality(StrEnum):
    Orange = "ORANGE"
    """五星"""
    Purple = "PURPLE"
    """四星"""
    Special = "SPECIAL"
    """特殊"""


class ItemType(StrEnum):
    Virtual = "VIRTUAL"
    Material = "MATERIAL"


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
    HealthPoints = "HP"
    """生命值"""
    HealthPointsPercent = "HPPercent"
    """生命值百分比"""

    Defense = "Defense"
    """防御力"""
    DefensePercent = "DefensePercent"
    """防御力百分比"""

    Attack = "Attack"
    """攻击力"""
    AttackPercent = "AttackPercent"
    """攻击力百分比"""

    CriticalRate = "Critical"
    """暴击率"""
    CriticalHurtRate = "CriticalHurt"
    """暴击伤害"""

    HealAdd = "HealAdd"
    """治疗加成"""
    ElementMastery = "ElementMastery"
    """元素精通"""
    ChargeEfficiency = "ChargeEfficiency"
    """元素充能效率"""

    PhysicalAddHurt = "Physical"
    """物理伤害加成"""
    PyroAddHurt = "Pyro"
    """火元素伤害加成"""
    HydroAddHurt = "Hydro"
    """水元素伤害加成"""
    AnemoAddHurt = "Anemo"
    """风元素伤害加成"""
    ElectroAddHurt = "Electro"
    """雷元素伤害加成"""
    DendroAddHurt = "Dendro"
    """草元素伤害加成"""
    CryoAddHurt = "Cryo"
    """冰元素伤害加成"""
    GeoAddHurt = "Geo"
    """岩元素伤害加成"""


class FoodQuality(StrEnum):
    STRANGE = "Strange"
    """奇怪的"""
    ORDINARY = "Ordinary"
    """普通的"""
    DELICIOUS = "Delicious"
    """美味的"""


class Association(StrEnum):
    Inazuma = "INAZUMA"
    """稻妻"""
    Mondstadt = "MONDSTADT"
    """蒙德"""
    Liyue = "LIYUE"
    """璃月"""
    Sumeru = "SUMERU"
    """须弥"""
    Fontaine = "FONTAINE"
    """枫丹"""
    Natlan = "NATLAN"
    """纳塔"""
    Snezhnaya = "SNEZHNAYA"
    """至冬"""

    Mainactor = "MAINACTOR"
    """主角"""
    Fatui = "FATUI"
    """愚人众"""
    Ranger = "RANGER"
    """游侠"""
