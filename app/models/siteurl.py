from sqlalchemy import Column, String, Text, Integer, DateTime

from app.models.base_class import Base
from app.models.model_helpers import utcnow


class SiteUrl(Base):
    """
    Columns:
    - id: int, primary_key
    - url: str
    - parent: str, foreign_key
    - html: str
    - text: str
    - created_date: datetime
    - updated_date: datetime

    """

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False, index=True)
    domain = Column(String, unique=False, nullable=False)
    text = Column(Text)
    html = Column(Text)
    ts_created = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
    ts_updated = Column(
        DateTime(timezone=True),
        server_onupdate=utcnow(),
        server_default=utcnow(),
        nullable=False,
    )
