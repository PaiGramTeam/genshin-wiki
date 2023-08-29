from peewee import IntegerField, CharField
from genshin.wiki._database._mode import Model, MapStringField


class Item(Model):
    name = MapStringField()
    """Name of the item."""

    description = MapStringField()
    """Description of the item."""
