from itertools import chain

from model.avatar import AvatarBirth, AvatarInfo, AvatarStories, Seuyu, Story
from model.enums import Association, AvatarQuality, Element, WeaponType
from utils.const import PROJECT_ROOT
from utils.manager import ResourceManager
from utils.typedefs import Lang

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

        breakpoint()
