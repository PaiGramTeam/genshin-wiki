from enum import StrEnum

from utils.model import BaseModel


class ItemType(StrEnum):
    ...


class Item(BaseModel):
    id: int
    """ID"""
    name: str
    """名称"""
    family: str
    """种类"""
    type: str | None
    """类型"""
    icon: str
    """图标名"""
    rarity: int | None
    """星级"""
    description: str
    """描述"""
    special_description: str | None
    """特殊描述"""


class MaterialType(StrEnum):
    ADSORBATE = "Adsorbate"
    FAKE_ABSORBATE = "Fake_Absorbate"

    CONSUME = "消费物"
    TALENT = "天赋"
    AVATAR = "角色"
    CHEST = "宝箱"
    NOTICE_ADD_HP = "NOTICE_ADD_HP"
    EXCHANGE = "交换物"
    WOOD = "木材"
    QUEST = "任务"
    CRICKET = "蟋蟀"
    WIDGET = "Widget"
    ELEM_CRYSTAL = "Elem_Crystal"
    SPICE_FOOD = "Spice_Food"
    ACTIVITY_GEAR = "Activity_Gear"
    ACTIVITY_ROBOT = "Activity_Robot"
    ACTIVITY_JIGSAW = "Activity_Jigsaw"
    FOOD = "Food"
    EXP_FRUIT = "Exp_Fruit"
    WEAPON_EXP_STONE = "Weapon_Exp_Stone"
    AVATAR_MATERIAL = "Avatar_Material"
    RELIQUARY_MATERIAL = "Reliquary_Material"
    CONSUME_BATCH_USE = "Consume_Batch_Use"
    FISH_BAIT = "Fish_Bait"
    CHEST_BATCH_USE = "Chest_Batch_Use"
    SELECTABLE_CHEST = "Selectable_Chest"
    HOME_SEED = "Home_Seed"
    FLYCLOAK = "Flycloak"
    BGM = "Bgm"
    SEA_LAMP = "Sea_Lamp"
    CHANNELLER_SLAB_BUFF = "Channeller_Slab_Buff"
    FISH_ROD = "Fish_Rod"
    NAMECARD = "Namecard"
    ARANARA = "Aranara"
    DESHRET_MANUAL = "Deshret_Manual"
    FIREWORKS = "Fireworks"
    COSTUME = "Costume"
    FURNITURE_SUITE_FORMULA = "Furniture_Suite_Formula"
    FURNITURE_FORMULA = "Furniture_Formula"


class Material(Item):
    material_type: MaterialType
    """材料类型"""


class FoodQuality(StrEnum):
    STRANGE = "Strange"
    """奇怪的"""
    ORDINARY = "Ordinary"
    """普通的"""
    DELICIOUS = "Delicious"
    """美味的"""


class Food(Item):
    quality: FoodQuality | None
    """食物质量"""
    effect: str
    """效果"""
