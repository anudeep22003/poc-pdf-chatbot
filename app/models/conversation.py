from sqlalchemy import Column, String, Text, Integer, DateTime

from app.models.base_class import Base
from app.models.model_helpers import utcnow


class Conversation(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    domain = Column(Text)
    ts_created = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
