from sqlalchemy import Column, String, Text, Integer, DateTime, Float

from app.models.base_class import Base
from app.models.model_helpers import utcnow


class Message(Base):
    conv_id = Column(Integer, nullable=False)
    content = Column(Text)
    sender = Column(String, nullable=False)  # human
    receiver = Column(String, nullable=False)  # agent
    sources = Column(String)
    ts_created = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
    response_time = Column(Float)


if __name__ == "__main__":
    ...
