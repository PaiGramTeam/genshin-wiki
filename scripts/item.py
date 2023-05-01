from pathlib import Path

import ujson as json
from aiofiles import open as async_open

from model.enums import FoodQuality, ItemType, MaterialType
from model.item import Food, Item, Material, Namecard
from utils.const import PROJECT_ROOT
from utils.manager import ResourceManager
from utils.typedefs import Lang

OUT_DIR = PROJECT_ROOT.joinpath("out")


# noinspection PyShadowingBuiltins
async def parse_item_data(
    lang: Lang,
) -> tuple[Path, list[Item | Material | Food | Namecard]]:
    out_path = OUT_DIR.joinpath(f"{lang}")
    out_path.mkdir(exist_ok=True, parents=True)

    manager = ResourceManager(lang=lang)
    json_data = manager.fetch("MaterialExcelConfigData")

    item_list = []
    for data in filter(lambda x: "rankLevel" in x, json_data):
        id = data["id"]
        if name := manager.get_text(data["nameTextMapHash"]) is None:
            continue
        type = manager.get_text(data["typeDescTextMapHash"])
        icon = data["icon"]
        rarity = data["rankLevel"]
        description = manager.get_text(data["descTextMapHash"]) or ""
        special_description = manager.get_text(data["specialDescTextMapHash"])
        item_type = ItemType(data["itemType"].removeprefix("ITEM_"))

        kwargs = {
            "id": id,
            "name": name,
            "type": type,
            "icon": icon,
            "rarity": rarity,
            "description": description,
            "special_description": special_description,
            "item_type": item_type,
        }

        try:
            if "picPath" in data and data["picPath"]:
                pictures = data["picPath"]
                item = Namecard(pictures=pictures, **kwargs)

            elif "materialType" in data:
                material_type = MaterialType(
                    data["materialType"].removeprefix("MATERIAL_")
                )
                item = Material(material_type=material_type, **kwargs)
            elif "foodQuality" in data:
                quality = FoodQuality(data["foodQuality"])
                effect = manager.get_text(data["effectDescTextMapHash"])
                effect_icon = data["effectIcon"]
                effect_name = data["effectName"]
                item = Food(
                    quality=quality,
                    effect=effect,
                    effect_icon=effect_icon,
                    effect_name=effect_name,
                    **kwargs,
                )
            else:
                item = Item(**kwargs)
        except Exception as e:
            breakpoint()
            raise e

        item_list.append(item)
    async with async_open(out_path / "item.json", encoding="utf-8", mode="w") as file:
        await file.write(
            json.dumps(
                [i.dict() for i in item_list],
                ensure_ascii=False,
                encode_html_chars=False,
                indent=4,
            ),
        )
    return out_path, item_list
