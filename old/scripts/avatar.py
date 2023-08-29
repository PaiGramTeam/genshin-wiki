from functools import lru_cache
from itertools import chain
from logging import getLogger

from ormar import QuerySet

from models.avatar import (
    Avatar,
    AvatarIcon,
    AvatarBirthday,
    AvatarSeuyu,
    AvatarStory,
    AvatarStories,
)
from models.enums import Association, AvatarQuality, Element, WeaponType
from utils.manager import ResourceManager
from utils.typedefs import Lang

logger = getLogger(__name__)


avatar_query_set: QuerySet[Avatar] = Avatar.objects
avatar_icon_query_set: QuerySet[AvatarIcon] = AvatarIcon.objects
avatar_birthday_query_set: QuerySet[AvatarBirthday] = AvatarBirthday.objects
avatar_seuyu_query_set: QuerySet[AvatarSeuyu] = AvatarSeuyu.objects
avatar_story_query_set: QuerySet[AvatarStory] = AvatarStory.objects
avatar_stories_query_set: QuerySet[AvatarStories] = AvatarStories.objects


@lru_cache
def get_element_data() -> dict[Element, set[int]]:
    _manager = ResourceManager("chs")
    _avatar_json_data = _manager.fetch("AvatarExcelConfigData")
    _fetter_info_json_data = _manager.fetch("FetterInfoExcelConfigData")
    text_map = {
        "火": Element.Pyro,
        "水": Element.Hydro,
        "风": Element.Anemo,
        "雷": Element.Electro,
        "草": Element.Dendro,
        "冰": Element.Cryo,
        "岩": Element.Geo,
        "无": Element.Null,
    }
    result = {k: set() for k in text_map.values()}
    for data in _avatar_json_data:
        _id = data["id"]
        if (
            info_data := next(
                chain(
                    filter(lambda x: x["avatarId"] == _id, _fetter_info_json_data),
                    [None],
                )
            )
        ) is None:
            continue
        if (
            vision := _manager.get_text(
                text_id := info_data["avatarVisionBeforTextMapHash"]
            )
        ) is not None:
            result[text_map[vision]] = set(list(result[text_map[vision]]) + [text_id])
    return result


# noinspection PyUnusedLocal,PyShadowingBuiltins
async def parse_avatar_data(lang: Lang):
    manager = ResourceManager(lang)
    avatar_data_list: list[dict] = manager.fetch("AvatarExcelConfigData")
    fetter_info_data_list = manager.fetch("FetterInfoExcelConfigData")
    story_data_list = manager.fetch("FetterStoryExcelConfigData")
    promote_data_list = manager.fetch("AvatarPromoteExcelConfigData")
    avatar_hero_data_list = manager.fetch("AvatarHeroEntityExcelConfigData")

    skill_depot_data_list = manager.fetch("AvatarSkillDepotExcelConfigData")
    skill_data_list = manager.fetch("AvatarSkillExcelConfigData")
    proud_skill_data_list = manager.fetch("ProudSkillExcelConfigData")
    talent_data_list = manager.fetch("AvatarTalentExcelConfigData")
    cook_bonus_data_list = manager.fetch("CookBonusExcelConfigData")

    for data in avatar_data_list:
        id = data["id"]

        info_data = next(
            chain(filter(lambda x: x["avatarId"] == id, fetter_info_data_list), [None])
        )
        if info_data is None:
            continue

        name = manager.get_text(data["nameTextMapHash"])
        icon, _ = await avatar_icon_query_set.get_or_create(
            icon_name=data["iconName"], side_icon_name=data["sideIconName"]
        )
        element = next(
            filter(
                lambda x: info_data["avatarVisionBeforTextMapHash"] in x[1],
                get_element_data().items(),
            )
        )[0]
        quality = AvatarQuality(
            data["qualityType"].removeprefix("QUALITY_").replace("ORANGE_SP", "SPECIAL")
        )
        weapon_type = next(
            filter(
                lambda x: x in data["weaponType"].replace("POLE", "POLEARM"),
                WeaponType.__members__.values(),
            )
        )
        ###########################################
        ###############  角色信息  #################
        ###########################################
        title = manager.get_text(info_data["avatarTitleTextMapHash"])
        birth, _ = (
            (
                await avatar_birthday_query_set.get_or_create(
                    month=info_data["infoBirthMonth"], day=info_data["infoBirthDay"]
                )
            )
            if id not in list(map(lambda x: x["avatarId"], avatar_hero_data_list))
            else (None, False)
        )
        occupation = manager.get_text(info_data["avatarNativeTextMapHash"])
        vision = manager.get_text(info_data["avatarVisionBeforTextMapHash"])
        constellation = manager.get_text(
            info_data["avatarConstellationBeforTextMapHash"]
        )
        description = manager.get_text(info_data["avatarDetailTextMapHash"])
        association = Association(
            info_data["avatarAssocType"].removeprefix("ASSOC_TYPE_")
        )
        seuyu, _ = await avatar_seuyu_query_set.get_or_create(
            chinese=manager.get_text(info_data["cvChineseTextMapHash"]),
            japanese=manager.get_text(info_data["cvJapaneseTextMapHash"]),
            english=manager.get_text(info_data["cvEnglishTextMapHash"]),
            korean=manager.get_text(info_data["cvKoreanTextMapHash"]),
        )

        story_list: list[AvatarStory] = []
        story_datas = sorted(
            filter(lambda x: x["avatarId"] == id, story_data_list),
            key=lambda x: x["fetterId"],
        )
        for story_data in story_datas:
            tips = list(
                filter(
                    lambda x: x is not None,
                    map(lambda x: manager.get_text(x), story_data["tips"]),
                )
            )
            story, _ = await avatar_story_query_set.get_or_create(
                title=manager.get_text(story_data["storyTitleTextMapHash"]),
                content=manager.get_text(story_data["storyContextTextMapHash"]),
                tips=tips,
            )
            story_list.append(story)
        avatar_stories, _ = await avatar_stories_query_set.get_or_create(
            **{
                i[0]: i[1]
                for i in zip(
                    filter(lambda x: x != "id", AvatarStories.__fields__), story_list
                )
            }
        )

        breakpoint()
