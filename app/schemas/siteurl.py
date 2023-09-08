import typing as t
from datetime import datetime
from pydantic import BaseModel


class SiteUrlBase(BaseModel):
    url: str
    domain: str
    text: t.Optional[str] = ""
    html: t.Optional[str] = ""


class SiteUrlCreate(SiteUrlBase):
    pass


class SiteUrlUpdateHtml(SiteUrlBase):
    html: str


class SiteUrlUpdateText(SiteUrlBase):
    text: str


class SiteUrl(SiteUrlBase):
    id: int
    ts_created: datetime
    ts_updated: datetime

    class Config:
        orm_mode = True
