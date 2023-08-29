from ormar import Integer

from models._base import Model, ModelMeta

__all__ = ("ItemCount", )



class ItemCount(Model):
    class Meta(ModelMeta):
        tablename = 'item_count'

    id: int = Integer(primary_key=True)
    """ID"""

    item_id: int = Integer()
    """物品ID"""
    count: int = Integer()
    """数量"""

ModelMeta.metadata.create_all()