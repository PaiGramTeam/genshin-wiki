from genshin.wiki.config import genshin_wiki_config, use_genshin_wiki_config


def main():
    print(genshin_wiki_config.lang)
    with use_genshin_wiki_config(lang="EN"):
        print(genshin_wiki_config.lang)
    print(genshin_wiki_config.lang)


if __name__ == "__main__":
    main()
