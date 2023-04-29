from scripts.avatar import parse_avatar_data
from scripts.item import parse_item_data
from utils.typedefs import Lang


async def parse(lang: Lang):
    await parse_item_data(lang)
    await parse_avatar_data(lang)


async def main():
    for lang in Lang.__args__:
        await parse(lang)


def __main__():
    import asyncio

    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())


if __name__ == "__main__":
    __main__()
