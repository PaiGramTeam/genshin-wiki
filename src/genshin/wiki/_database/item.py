from peewee import IntegerField, CharField
from genshin.wiki._mode import Model


class Item(Model):
    name = CharField()
