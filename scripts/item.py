from model.enums import ItemType
from utils.manager import ResourceManager
from utils.typedefs import Lang


# noinspection PyShadowingBuiltins
async def parse_item_data(lang: Lang):
    manager = ResourceManager(lang=lang)
    json_data = manager.fetch("MaterialExcelConfigData")
    for data in json_data:
        id = data["id"]
        name = manager.get_text(data["nameTextMapHash"])
        type = manager.get_text(data["typeDescTextMapHash"])
        icon = data["icon"]
        rarity = data["rankLevel"]
        description = manager.get_text(data["descTextMapHash"])
        special_description = manager.get_text(data["specialDescTextMapHash"])
        item_type = ItemType(data["itemType"].removeprefix('ITEM_'))
    breakpoint()
