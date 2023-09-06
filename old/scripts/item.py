from ormar import QuerySet

from models.enums import FoodQuality
from utils.manager import ResourceManager
from utils.typedefs import Lang
from models.item import OldItem
import regex as re

try:
    from loguru import logger
except ImportError:
    from logging import getLogger

    logger = getLogger(__name__)

# noinspection PyShadowingBuiltins
async def parse_item_data(lang: Lang):
    manager = ResourceManager(lang)
    item_data_list: list[dict] = manager.fetch("MaterialExcelConfigData")
    item_query_set: QuerySet[OldItem] = OldItem.objects
    for item_data in item_data_list:
        id = item_data["id"]

        name = manager(item_data["nameTextMapHash"])
        if name is None or re.findall(r"^[(（].*?[)）]", name):  # 跳过无名称和测试物品
            continue

        type = manager.get_text(item_data["typeDescTextMapHash"])
        icon = item_data["icon"]
        rarity = item_data.get("rankLevel", 5) % 100
        description = manager.get_text(item_data["descTextMapHash"])
        special_description = manager.get_text(item_data["specialDescTextMapHash"])
        is_virtual = item_data["itemType"] == "ITEM_VIRTUAL"

        kwargs = {}
        if (
            "foodQuality" in item_data
            or item_data.get("materialType", None) == "MATERIAL_FOOD"
        ):
            if "foodQuality" in item_data:
                kwargs["quality"] = FoodQuality(
                    item_data["foodQuality"].removeprefix("FOOD_QUALITY_").title()
                )
            kwargs["effect"] = manager.get_text(item_data["effectDescTextMapHash"])
            kwargs["effect_icon"] = item_data["effectIcon"]
            kwargs["cd_time"] = item_data.get("cdTime", None)
            kwargs["cd_group"] = item_data.get("cdGroup", None)

        if "picPath" in item_data and item_data["picPath"]:
            kwargs["pictures"] = item_data["picPath"]

        if "materialType" in item_data:
            kwargs["material_type"] = item_data["materialType"].removeprefix(
                "MATERIAL_"
            )
            kwargs["material_type_description"] = manager.get_text(
                item_data["typeDescTextMapHash"]
            )

        kwargs["close_bag_after_used"] = item_data.get("closeBagAfterUsed", None)
        kwargs["interaction_title"] = manager.get_text(
            item_data["interactionTitleTextMapHash"]
        )
        kwargs["interaction_description"] = manager.get_text(
            item_data.get("interactionDescTextMapHash", None)
        )
        kwargs["is_force_get_hint"] = item_data.get("isForceGetHint", None)
        kwargs["no_first_get_hint"] = item_data.get("noFirstGetHint", None)
        kwargs["use_on_gain"] = item_data.get("useOnGain", None)
        kwargs["use_target"] = item_data.get("useTarget", None)

        item, _ = await item_query_set.get_or_create(
            id=id,
            name=name,
            type=type,
            icon=icon,
            rarity=rarity,
            description=description,
            special_description=special_description,
            is_virtual=is_virtual,
            **{k: v for k, v in kwargs.items() if v is not None},
        )
        logger.info(f"Item: {item.name} {item.type} {item.material_type}")
    breakpoint()
