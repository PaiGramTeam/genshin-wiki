from utils.model import BaseModel


class ItemCount(BaseModel):
    item_id: int
    """物品ID"""
    count: int
    """数量"""
