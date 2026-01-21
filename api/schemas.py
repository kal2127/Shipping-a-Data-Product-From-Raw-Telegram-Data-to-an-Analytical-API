from pydantic import BaseModel
from typing import List, Optional

class ProductStats(BaseModel):
    term: str
    mention_count: int

class ChannelActivity(BaseModel):
    date: str
    post_count: int

class MessageResult(BaseModel):
    message_id: str
    channel_title: str
    text: Optional[str]
    view_count: Optional[int]

class VisualStats(BaseModel):
    image_category: str
    total_count: int
    avg_views: float