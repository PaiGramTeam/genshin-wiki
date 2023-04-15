import asyncio

from utils.const import PROJECT_ROOT
from utils.context import ContextManager
from utils.manager import ResourceManager
from utils.text import Text
from utils.typedefs import Lang
import ujson as json

OUTPUT_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# noinspection PyShadowingBuiltins
async def parse_item_data(resource: ResourceManager):
    from models.item import Food, FoodQuality, Item

    json_data = resource.fetch("MaterialExcelConfigData")
    data_list = []

    for item_data in json_data:
        id = item_data["id"]
        name = Text(item_data["nameTextMapHash"])
        family = item_data.get("materialType", "")
        rarity = item_data.get("rankLevel")
        type = Text(item_data["typeDescTextMapHash"])
        icon = item_data["icon"]
        description = Text(item_data["descTextMapHash"])
        special = Text(item_data["specialDescTextMapHash"]) or None

        base_kwargs = {
            "id": id,
            "name": name,
            "family": family,
            "rarity": rarity,
            "type": type,
            "icon": icon,
            "description": description,
        }
        if special is not None:
            base_kwargs["special_description"] = special

        if "materialType" in item_data:  # 材料
            material_type = item_data["materialType"]

        elif "foodQuality" in item_data:  # 食物
            quality = FoodQuality(
                item_data["foodQuality"].removeprefix("FOOD_QUALITY_").title()
            )
            effect = Text(item_data["effectDescTextMapHash"])
            item = Food(quality=quality, effect=effect, **base_kwargs)
        else:
            item = Item(**base_kwargs)
        data_list.append(item.dict(exclude_none=True))

    item_data_file = OUTPUT_DIR / "item.json"
    with open(item_data_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(data_list, ensure_ascii=False))
    breakpoint()


async def fetch_parse_data(lang: Lang):
    with ContextManager().with_context(
        "resource_manager", ResourceManager(lang=lang)
    ) as resource_manager:
        await parse_item_data(resource_manager)


async def main():
    task_list = []
    for lang in Lang.__args__:
        task = asyncio.create_task(fetch_parse_data(lang=lang))
        task_list.append(task)
    await asyncio.gather(*task_list)


def __main__():
    import asyncio

    import sys

    if (3, 10) >= sys.version_info >= (3, 8) and sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())


if __name__ == "__main__":
    __main__()
