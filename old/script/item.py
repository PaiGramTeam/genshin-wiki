import regex as re
from ormar import QuerySet

from genshin_wiki.config import with_genshin_wiki_config
from genshin_wiki.item import Item, ItemDescription
from genshin_wiki.manager import resource_manager
from genshin_wiki.tools.typedefs import Lang

item_query_set: QuerySet[Item] = Item.objects
item_description_query_set: QuerySet[ItemDescription] = ItemDescription.objects


async def parse_item_data(lang: Lang = "chs"):
    with with_genshin_wiki_config(lang=lang):
        item_data_list: list[dict] = resource_manager.fetch_metadata(
            "MaterialExcelConfigData"
        )
        item_codex_data_list: list[dict] = resource_manager.fetch_metadata(
            "MaterialCodexExcelConfigData"
        )
        item_source_data_list: list[dict] = resource_manager.fetch_metadata(
            "MaterialSourceDataExcelConfigData"
        )

        for item_data in item_data_list:
            id = item_data["id"]

            name = item_data["nameTextMapHash"]
            if (true_name := resource_manager.get_text(name)) is None or re.findall(
                r"^[(（].*?[)）]", true_name
            ):  # 跳过无名称和测试物品
                continue

            type = item_data["typeDescTextMapHash"]
            icon = item_data["icon"]
            rarity = item_data.get("rankLevel", 5) % 100

            main_description = item_data["descTextMapHash"]
            code_description = next(
                filter(lambda x: x["materialId"] == id, item_codex_data_list),
                {"descTextMapHash": None},
            )["descTextMapHash"]
            special_description = item_data["specialDescTextMapHash"]

            description, _ = await item_description_query_set.get_or_create(
                id=id,
                main=main_description,
                codex=code_description,
                special=special_description,
            )

            source_item = next(
                filter(lambda x: x["id"] == id, item_source_data_list),
                {"jumpList": [], "textList": []},
            )
            source = list(
                set(
                    filter(
                        lambda x: resource_manager.get_text(x) is not None,
                        source_item["jumpList"] + source_item["textList"],
                    )
                )
            ) or None
            item, _ = await item_query_set.get_or_create(
                id=id,
                name=name,
                type=type,
                rarity=rarity,
                _source=source,
                description=description,
            )
            if source:
                print()
                print(source)
                print(item._source)
                breakpoint()

        breakpoint()
