import typing as t
from datetime import datetime
from pydantic import BaseModel


class ConversationBase(BaseModel):
    pass


class ConversationCreate(ConversationBase):
    domain: str
    pass


class Conversation(ConversationBase):
    id: int
    ts_created: datetime

    class Config:
        orm_mode = True
