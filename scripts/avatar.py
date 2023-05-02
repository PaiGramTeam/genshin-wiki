from itertools import chain
from typing import TypeVar

import ujson as json
from aiofiles import open as async_open
from humps import pascalize

from model.avatar import (
    AddProp,
    AlternateSprint,
    Avatar,
    AvatarAttribute,
    AvatarBirth,
    AvatarConstellation,
    AvatarInfo,
    AvatarPromote,
    AvatarStories,
    AvatarTalents,
    CombatTalent,
    ElementalBurst,
    ElementalSkill,
    FirstAscensionPassive,
    FourthAscensionPassive,
    MiscellaneousPassive,
    NormalAttack,
    PassiveTalent,
    Seuyu,
    Story,
    Talent,
    TalentAttribute,
    UtilityPassive,
)
from model.enums import Association, AvatarQuality, Element, PropType, WeaponType
from model.other import ItemCount
from utils.const import PROJECT_ROOT
from utils.funcs import remove_rich_tag
from utils.manager import ResourceManager
from utils.typedefs import Lang

try:
    import regex as re
except ImportError:
    import re

TalentType = TypeVar("TalentType", bound=Talent)

OUT_DIR = PROJECT_ROOT.joinpath("out")

elements_map = {
    (
        230082676,
        313529204,
        627825788,
        1247335084,
        1646245548,
        1740638908,
        3105283268,
        3112476852,
        3177381772,
        3847511308,
    ): Element.Pyro,
    (
        321258364,
        483165900,
        756679372,
        1688473500,
        2480954540,
        3228108484,
        3400532572,
        3646588372,
        4022324356,
    ): Element.Hydro,
    (
        126875444,
        467004516,
        550531300,
        898621369,
        1778251796,
        2075460644,
        2477900860,
        2648184060,
    ): Element.Anemo,
    (
        122554396,
        608089036,
        689445588,
        1072755468,
        1821644548,
        1843086100,
        2085306033,
        2143937940,
        2480172868,
        2689029804,
        3352621156,
        4219874220,
    ): Element.Electro,
    (2161032364, 4017448612): Element.Dendro,
    (
        98482612,
        766902996,
        862088588,
        1480674860,
        1695600284,
        2778487532,
        2809830820,
        3057990932,
        4127670180,
        4220569804,
    ): Element.Cryo,
    (
        825986772,
        967031460,
        1016213980,
        1662907292,
        2507042785,
        3219124204,
        3617274620,
        3929787020,
    ): Element.Geo,
    (471154292, 821712868, 1128382182, 3053155130, 4168416172): Element.Null,
}
prop_type_map = {
    "Hp": PropType.HP,
    "RockAddHurt": PropType.Geo,
    "ElecAddHurt": PropType.Electro,
    "FireAddHurt": PropType.Pyro,
    "WaterAddHurt": PropType.Hydro,
    "IceAddHurt": PropType.Cryo,
    "WindAddHurt": PropType.Anemo,
    "GrassAddHurt": PropType.Dendro,
}


def get_skill_attributes(
    proud_skill_group_id: int,
) -> tuple[list[TalentAttribute], list[str]]:
    proud_skill_datas = sorted(
        filter(
            lambda x: x["proudSkillGroupId"] == proud_skill_group_id,
            proud_skill_json_data,
        ),
        key=lambda x: x["level"],
    )
    result: list[TalentAttribute] = []
    param_descriptions: list[str] = []
    for proud_skill_data in proud_skill_datas:
        param_descriptions = list(
            filter(
                lambda x: x is not None,
                map(
                    lambda x: manager.get_text(x),
                    proud_skill_data["paramDescList"],
                ),
            )
        )
        param_num = len(param_descriptions)
        for param_description in param_descriptions:
            param_num = max(
                param_num,
                *map(int, re.findall(r"param(\d*)\:", param_description)),
            )
        result.append(
            TalentAttribute(
                level=proud_skill_data["level"],
                params=proud_skill_data["paramList"][:param_num],
                break_level=proud_skill_data.get("breakLevel", 0),
                coin=proud_skill_data.get("coinCost", 0),
                cost_items=list(
                    map(
                        lambda x: ItemCount(item_id=x["id"], count=x["count"]),
                        filter(lambda x: x, proud_skill_data["costItems"]),
                    )
                ),
            )
        )
    return result, param_descriptions


def parse_skill(skill_id: int, skill_cls: type[CombatTalent]) -> CombatTalent:
    skill_data = next(filter(lambda x: x["id"] == skill_id, skill_json_data))
    _name = manager.get_text(skill_data["nameTextMapHash"])
    _description = manager.get_text(skill_data["descTextMapHash"])
    icon = skill_data["skillIcon"]
    cooldown = (
        skill_data.get("cdTime", 0) if "cooldown" in skill_cls.__fields__ else None
    )
    attributes, param_descriptions = get_skill_attributes(
        skill_data["proudSkillGroupId"]
    )
    return skill_cls(
        **{
            i[0]: i[1]
            for i in zip(
                [
                    "name",
                    "description",
                    "icon",
                    "cooldown",
                    "attributes",
                    "param_descriptions",
                ],
                [_name, _description, icon, cooldown, attributes, param_descriptions],
            )
            if i is not None
        }
    )


def parse_passive_talent(
    talent_data: dict, talent_cls: type[PassiveTalent]
) -> PassiveTalent:
    group_id = talent_data["proudSkillGroupId"]
    _promote_level = talent_data.get("needAvatarPromoteLevel", 0)
    skill_data = next(
        filter(lambda x: x["proudSkillGroupId"] == group_id, proud_skill_json_data)
    )
    param_descriptions = list(
        filter(
            lambda x: x is not None,
            map(
                lambda x: manager.get_text(x),
                skill_data["paramDescList"],
            ),
        )
    )
    _description = manager.get_text(skill_data["descTextMapHash"])
    _param_list = skill_data["paramList"][
        : len(re.findall(r"(\d+(?:\.)?\d+)", remove_rich_tag(_description) or ""))
    ]
    return talent_cls(
        name=manager.get_text(skill_data["nameTextMapHash"]) or "",
        description=_description or "",
        icon=skill_data["icon"],
        promote_level=_promote_level,
        param_descriptions=param_descriptions,
        attribute=TalentAttribute(
            params=_param_list,
            break_level=skill_data.get("breakLevel", 0),
        ),
    )


# noinspection PyShadowingBuiltins,SpellCheckingInspection,PyGlobalUndefined
async def parse_avatar_data(lang: Lang):
    global out_path, manager
    global avatar_json_data, fetter_info_json_data, story_json_data, promote_json_data
    global skill_depot_json_data, skill_json_data, proud_skill_json_data, talent_json_data
    out_path = OUT_DIR.joinpath(f"{lang}")
    out_path.mkdir(exist_ok=True, parents=True)

    manager = ResourceManager(lang=lang)
    avatar_json_data = manager.fetch("AvatarExcelConfigData")
    fetter_info_json_data = manager.fetch("FetterInfoExcelConfigData")
    story_json_data = manager.fetch("FetterStoryExcelConfigData")
    promote_json_data = manager.fetch("AvatarPromoteExcelConfigData")

    skill_depot_json_data = manager.fetch("AvatarSkillDepotExcelConfigData")
    skill_json_data = manager.fetch("AvatarSkillExcelConfigData")
    proud_skill_json_data = manager.fetch("ProudSkillExcelConfigData")
    talent_json_data = manager.fetch("AvatarTalentExcelConfigData")

    avatar_list = []
    for data in avatar_json_data:
        id = data["id"]
        if (
            info_data := next(
                chain(
                    filter(lambda x: x["avatarId"] == id, fetter_info_json_data), [None]
                )
            )
        ) is None:
            continue
        name = manager.get_text(data["nameTextMapHash"])
        element = next(
            filter(
                lambda x: info_data["avatarVisionBeforTextMapHash"] in x[0],
                elements_map.items(),
            )
        )[1]
        quality = AvatarQuality(
            data["qualityType"].removeprefix("QUALITY_").replace("ORANGE_SP", "SPECIAL")
        )
        weapon_type = next(
            filter(
                lambda x: x in data["weaponType"].replace("POLE", "POLEARM"),
                WeaponType.__members__.values(),
            )
        )

        # 角色信息
        title = manager.get_text(info_data["avatarTitleTextMapHash"])
        birth = (
            AvatarBirth(
                month=info_data["infoBirthMonth"], day=info_data["infoBirthDay"]
            )
            if id not in [10000005, 10000007]
            else None
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
        seuyu = Seuyu(
            cn=manager.get_text(info_data["cvChineseTextMapHash"]),
            jp=manager.get_text(info_data["cvJapaneseTextMapHash"]),
            en=manager.get_text(info_data["cvEnglishTextMapHash"]),
            kr=manager.get_text(info_data["cvKoreanTextMapHash"]),
        )
        story_datas = sorted(
            filter(lambda x: x["avatarId"] == id, story_json_data),
            key=lambda x: x["fetterId"],
        )
        stories = []
        for story_data in sorted(
            filter(lambda x: x["avatarId"] == id, story_datas),
            key=lambda x: x["fetterId"],
        ):
            tips = list(
                filter(
                    lambda x: x is not None,
                    map(lambda x: manager.get_text(x), story_data["tips"]),
                )
            )
            story = Story(
                title=manager.get_text(story_data["storyTitleTextMapHash"]),
                content=manager.get_text(story_data["storyContextTextMapHash"]),
                tips=tips,
            )
            stories.append(story)

        avatar_stories = AvatarStories(
            **{i[0]: i[1] for i in zip(AvatarStories.__fields__, stories)}
        )
        information = AvatarInfo(
            title=title,
            birth=birth,
            occupation=occupation,
            vision=vision,
            constellation=constellation,
            description=description,
            association=association,
            seuyu=seuyu,
            stories=avatar_stories,
        )

        # 角色基础属性
        attributes = AvatarAttribute(
            HP=data["hpBase"],
            Attack=data["attackBase"],
            Defense=data["defenseBase"],
            Critical=data["critical"],
            CriticalHurt=data["criticalHurt"],
            ChargeEfficiency=data["chargeEfficiency"],
        )

        # 天赋
        skill_depot_data = next(
            filter(lambda x: x["id"] == data["skillDepotId"], skill_depot_json_data)
        )
        skill_ids = list(filter(lambda x: x != 0, skill_depot_data["skills"]))
        # 普通攻击
        normal_attack = parse_skill(skill_ids[0], NormalAttack)
        # 冲刺技能
        alternate_sprint = (
            parse_skill(skill_ids[2], AlternateSprint) if len(skill_ids) == 3 else None
        )
        if id not in [10000005, 10000007]:
            # 元素战技
            elemental_skill = parse_skill(skill_ids[1], ElementalSkill)
            # 元素爆发
            burst_skill = parse_skill(skill_depot_data["energySkill"], ElementalBurst)
            # 第一次突破被动天赋
            first_passive = parse_passive_talent(
                skill_depot_data["inherentProudSkillOpens"][0], FirstAscensionPassive
            )
            # 第四次突破被动天赋
            fourth_passive = parse_passive_talent(
                skill_depot_data["inherentProudSkillOpens"][1], FourthAscensionPassive
            )
            # 实用固有天赋
            utility_passive = parse_passive_talent(
                skill_depot_data["inherentProudSkillOpens"][2], UtilityPassive
            )
        else:
            elemental_skill = (
                burst_skill
            ) = first_passive = fourth_passive = utility_passive = None
            # 杂项固有天赋
        if skill_depot_data["inherentProudSkillOpens"][3]:
            miscellaneous_passive = parse_passive_talent(
                skill_depot_data["inherentProudSkillOpens"][3], MiscellaneousPassive
            )
        else:
            miscellaneous_passive = None
        # noinspection PyTypeChecker
        avatar_talents = AvatarTalents(
            normal_attack=normal_attack,
            elemental_skill=elemental_skill,
            elemental_burst=burst_skill,
            alternate_sprint=alternate_sprint,
            first_ascension_passive=first_passive,
            fourth_ascension_passive=fourth_passive,
            utility_passive=utility_passive,
            miscellaneous_passive=miscellaneous_passive,
        )

        # 角色突破数据
        promote_id = data["avatarPromoteId"]
        promote_datas = sorted(
            filter(lambda x: x["avatarPromoteId"] == promote_id, promote_json_data),
            key=lambda x: x.get("promoteLevel", 0),
        )
        promotes = []
        for promote_data in promote_datas:
            items = []
            for item_data in promote_data["costItems"]:
                if item_data and id not in [10000005, 10000007]:
                    items.append(
                        ItemCount(item_id=item_data["id"], count=item_data["count"])
                    )
            add_props = []
            for add_prop_data in promote_data["addProps"]:
                _string = pascalize(
                    add_prop_data["propType"]
                    .removeprefix("FIGHT_PROP_")
                    .removeprefix("BASE_")
                    .lower()
                ).replace("Hp", "HP")
                prop_type_string = {
                    **prop_type_map,
                    **PropType.__members__,
                    **{v: v for k, v in PropType.__members__.items()},
                }[_string]
                prop_type = PropType(prop_type_string)
                add_props.append(
                    AddProp(
                        type=prop_type,
                        value=add_prop_data.get(
                            "value", attributes.dict().get(prop_type, 0)
                        ),
                    )
                )
            promotes.append(
                AvatarPromote(
                    promote_level=promote_data.get("promoteLevel", 0),
                    max_level=promote_data["unlockMaxLevel"],
                    add_props=add_props,
                    coin=promote_data.get("scoinCost", 0),
                    cost_items=items,
                )
            )

        # 角色命座信息
        constellations: list[AvatarConstellation] = []
        for constellation_id in filter(lambda x: x != 0, skill_depot_data["talents"]):
            constellation_data = next(
                filter(lambda x: x["talentId"] == constellation_id, talent_json_data)
            )
            constellation_description = manager.get_text(
                constellation_data["descTextMapHash"]
            )
            # noinspection PyTypeChecker
            constellations.append(
                AvatarConstellation(
                    name=manager.get_text(constellation_data["nameTextMapHash"]),
                    description=constellation_description,
                    icon=constellation_data["icon"],
                    param_list=list(
                        filter(lambda x: x != 0.0, constellation_data["paramList"])
                    ),
                )
            )
        avatar = Avatar(
            id=id,
            name=name,
            element=element,
            quality=quality,
            weapon_type=weapon_type,
            information=information,
            attributes=attributes,
            talents=avatar_talents,
            promotes=promotes,
            constellations=constellations,
        )
        avatar_list.append(avatar)

    async with async_open(out_path / "avatar.json", encoding="utf-8", mode="w") as file:
        await file.write(
            json.dumps(
                [i.dict(exclude_none=True) for i in avatar_list],
                ensure_ascii=False,
                encode_html_chars=False,
                indent=4,
            ),
        )
    return out_path, avatar_list
