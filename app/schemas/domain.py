import typing as T
from datetime import datetime
from pydantic import BaseModel


class DomainBase(BaseModel):
    domain: str
    pagerank: T.Optional[dict] = ""
    textrank: T.Optional[dict] = ""
    sitemap: T.Optional[str] = ""
    time_to_index: float


class DomainCreate(DomainBase):
    pass


class DomainUpdateTextrank(DomainBase):
    textrank: dict


class DomainUpdatePagerank(DomainBase):
    pagerank: dict


class Domain(DomainBase):
    id: int
    ts_created: datetime
    ts_updated: datetime

    class Config:
        orm_mode = True
