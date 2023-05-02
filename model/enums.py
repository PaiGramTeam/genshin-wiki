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


class FoodQuality(StrEnum):
    STRANGE = "Strange"
    """奇怪的"""
    ORDINARY = "Ordinary"
    """普通的"""
    DELICIOUS = "Delicious"
    """美味的"""


# noinspection SpellCheckingInspection
class MaterialType(StrEnum):
    Adsorbate = "ADSORBATE"
    FakeAbsorbate = "FAKE_ABSORBATE"
    Consume = "CONSUME"
    Talent = "TALENT"
    Avatar = "AVATAR"
    Chest = "CHEST"
    NoticeAddHp = "NOTICE_ADD_HP"
    Exchange = "EXCHANGE"
    Wood = "WOOD"
    Quest = "QUEST"
    Cricket = "CRICKET"
    Widget = "WIDGET"
    ElemCrystal = "ELEM_CRYSTAL"
    SpiceFood = "SPICE_FOOD"
    ActivityGear = "ACTIVITY_GEAR"
    ActivityRobot = "ACTIVITY_ROBOT"
    ActivityJigsaw = "ACTIVITY_JIGSAW"
    Food = "FOOD"
    ExpFruit = "EXP_FRUIT"
    WeaponExpStone = "WEAPON_EXP_STONE"
    AvatarMaterial = "AVATAR_MATERIAL"
    ReliquaryMaterial = "RELIQUARY_MATERIAL"
    ConsumeBatchUse = "CONSUME_BATCH_USE"
    FishBait = "FISH_BAIT"
    ChestBatchUse = "CHEST_BATCH_USE"
    SelectableChest = "SELECTABLE_CHEST"
    HomeSeed = "HOME_SEED"
    Flycloak = "FLYCLOAK"
    BGM = "BGM"
    SeaLamp = "SEA_LAMP"
    ChannellerSlabBuff = "CHANNELLER_SLAB_BUFF"
    FishRod = "FISH_ROD"
    Namecard = "NAMECARD"
    Aranara = "ARANARA"
    DeshretManual = "DESHRET_MANUAL"
    Fireworks = "FIREWORKS"
    Costume = "COSTUME"
    FurnitureSuiteFormula = "FURNITURE_SUITE_FORMULA"
    FurnitureFormula = "FURNITURE_FORMULA"


class Association(StrEnum):
    Inazuma = "INAZUMA"
    """稻妻"""
    Mondstadt = "MONDSTADT"
    """蒙德"""
    Mainactor = "MAINACTOR"
    """主角"""
    Liyue = "LIYUE"
    """璃月"""
    Fatui = "FATUI"
    """愚人众"""
    Ranger = "RANGER"
    """游侠"""
    Sumeru = "SUMERU"
    """须弥"""
