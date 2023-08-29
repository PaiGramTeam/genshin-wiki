from peewee import IntegerField, CharField
from genshin.wiki._database._mode import Model, MapTextField


# cdGroup
# cdTime
# closeBagAfterUsed
# descTextMapHash
# destroyReturnMaterial
# destroyReturnMaterialCount
# destroyRule
# effectDescTextMapHash
# effectGadgetID
# effectIcon
# effectName
# foodQuality
# gadgetId
# globalItemLimit
# icon
# id
# interactionTitleTextMapHash
# isForceGetHint
# isHidden
# isSplitDrop
# itemType
# itemUse
# materialType
# maxUseCount
# nameTextMapHash
# noFirstGetHint
# picPath
# playGainEffect
# rank
# rankLevel
# satiationParams
# setID
# specialDescTextMapHash
# stackLimit
# typeDescTextMapHash
# useLevel
# useOnGain
# useTarget
# weight
class Item(Model):
    name = MapTextField()
    """Name of the item."""

    description = MapTextField()
    """Description of the item."""

    special_description = MapTextField()
    """Special description of the item."""
