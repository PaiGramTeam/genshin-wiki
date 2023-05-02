from itertools import chain
from typing import TypeVar

from model.avatar import (
    AlternateSprint,
    AvatarAttribute,
    AvatarBirth,
    AvatarInfo,
    AvatarPromote,
    AvatarStories,
    ElementalBurst,
    ElementalSkill,
    NormalAttack,
    Seuyu,
    Story,
    Talent,
    TalentAttribute,
)
from model.enums import Association, AvatarQuality, Element, WeaponType
from model.other import ItemCount
from utils.const import PROJECT_ROOT
from utils.manager import ResourceManager
from utils.typedefs import Lang

try:
    import regex as re
except ImportError:
    import re

T = TypeVar("T", bound=Talent)

OUT_DIR = PROJECT_ROOT.joinpath("out")

elements = {
    3057990932: Element.Cryo,
    467004516: Element.Anemo,
    821712868: Element.Null,
    2480172868: Element.Electro,
    4022324356: Element.Hydro,
    627825788: Element.Pyro,
    2596397668: Element.Dendro,
    967031460: Element.Geo,
}


# noinspection PyShadowingBuiltins,SpellCheckingInspection
async def parse_avatar_data(lang: Lang):
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

    avatar_list = []
    for data in avatar_json_data:
        id = data["id"]
        if (
            info_data := next(
                chain(
                    filter(lambda x: x["avatarId"] == id, fetter_info_json_data),
                    [
                        None,
                    ],
                )
            )
        ) is None:
            continue
        name = manager.get_text(data["nameTextMapHash"])
        element = elements[info_data["avatarVisionBeforTextMapHash"]]
        quality = AvatarQuality(data["qualityType"].removeprefix("QUALITY_"))
        weapon_type = next(
            filter(lambda x: x in data["weaponType"], WeaponType.__members__.values())
        )

        # 角色信息
        title = manager.get_text(info_data["avatarTitleTextMapHash"])
        birth = AvatarBirth(
            month=info_data["infoBirthMonth"], day=info_data["infoBirthDay"]
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
        story_data = sorted(
            filter(lambda x: x["avatarId"] == id, story_json_data),
            key=lambda x: x["fetterId"],
        )
        stories = AvatarStories(
            **{
                i[0]: i[1]
                for i in zip(
                    AvatarStories.__fields__.keys(),
                    map(
                        lambda x: Story(
                            title=manager.get_text(x["storyTitleTextMapHash"]),
                            content=manager.get_text(x["storyContextTextMapHash"]),
                            tips=list(
                                filter(
                                    lambda y: y is not None,
                                    map(
                                        lambda z: manager.get_text(z),
                                        x["tips"],
                                    ),
                                )
                            ),
                        ),
                        sorted(
                            filter(lambda x: x["avatarId"] == id, story_data),
                            key=lambda x: x["fetterId"],
                        ),
                    ),
                )
            }
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
            stories=stories,
        )

        # 角色基础属性
        attribute = AvatarAttribute(
            HP=data["hpBase"],
            Attack=data["attackBase"],
            Defense=data["defenseBase"],
            Critical=data["critical"],
            CriticalDamage=data["criticalHurt"],
            ChargeEfficiency=data["chargeEfficiency"],
        )

        def get_skill_attributes(proud_skill_group_id: int) -> list[TalentAttribute]:
            proud_skill_datas = sorted(
                filter(
                    lambda x: x["proudSkillGroupId"] == proud_skill_group_id,
                    proud_skill_json_data,
                ),
                key=lambda x: x["level"],
            )
            result: list[TalentAttribute] = []
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
                        param_descriptions=param_descriptions,
                        param_list=proud_skill_data["paramList"][:param_num],
                        break_level=proud_skill_data.get("breakLevel", 0),
                        coin=proud_skill_data.get("coinCost", 0),
                        cost_items=list(
                            map(
                                lambda x: ItemCount(
                                    item_id=x["id"],
                                    count=x["count"],
                                ),
                                filter(lambda x: x, proud_skill_data["costItems"]),
                            )
                        ),
                    )
                )
            return result

        def parse_skill(skill_id: int, skill_cls: type[T]) -> T:
            skill_data = next(filter(lambda x: x["id"] == skill_id, skill_json_data))
            _name = manager.get_text(skill_data["nameTextMapHash"])
            _description = manager.get_text(skill_data["descTextMapHash"])
            icon = skill_data["skillIcon"]
            cooldown = (
                skill_data.get("cdTime", 0)
                if "cooldown" in skill_cls.__fields__.keys()
                else None
            )
            attributes = get_skill_attributes(skill_data["proudSkillGroupId"])
            return skill_cls(
                **{
                    i[0]: i[1]
                    for i in zip(
                        ["name", "description", "icon", "cooldown", "attributes"],
                        [_name, _description, icon, cooldown, attributes],
                    )
                    if i is not None
                }
            )

        # 天赋
        skill_depot_data = next(
            filter(lambda x: x["id"] == data["skillDepotId"], skill_depot_json_data)
        )
        skill_ids = list(filter(lambda x: x != 0, skill_depot_data["skills"]))
        # 普通攻击
        normal_attack = parse_skill(skill_ids[0], NormalAttack)
        # 元素战技
        elemental_skill = parse_skill(skill_ids[1], ElementalSkill)
        # 冲刺技能
        if len(skill_ids) == 3:
            alternate_sprint = parse_skill(skill_ids[2], AlternateSprint)
        # 元素爆发
        burst_skill = parse_skill(skill_depot_data["energySkill"], ElementalBurst)
        breakpoint()

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
                if item_data:
                    items.append(
                        ItemCount(item_id=item_data["id"], count=item_data["count"])
                    )
            promotes.append(
                AvatarPromote(
                    promote_level=promote_data.get("promoteLevel", 0),
                    max_level=promote_data["unlockMaxLevel"],
                    coin=promote_data.get("scoinCost", 0),
                    cost_items=items,
                )
            )
        breakpoint()
