from sqlalchemy import Column, String, Text, Integer, DateTime, PickleType, Float

from app.models.base_class import Base
from app.models.model_helpers import utcnow


class Domain(Base):
    """
    Columns:
    - id: int, primary_key
    - domain: str
    - pagerank: json
    - textrank: json
    - sitemap: str
    - ts_created: datetime
    - ts_updated: datetime
    - time_to_index: float
    """

    # generate column definitions
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, nullable=False, index=True)
    pagerank = Column(PickleType)
    textrank = Column(PickleType)
    sitemap = Column(Text)
    ts_created = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
    ts_updated = Column(
        DateTime(timezone=True),
        server_default=utcnow(),
        server_onupdate=utcnow(),
        nullable=False,
    )
    time_to_index = Column(Float)
