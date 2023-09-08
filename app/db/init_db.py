from app import crud, schemas
from app.default_data import message_data
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)


def init_db(db: Session):
    message_in = schemas.MessageCreate(**message_data)
    created_message = crud.message.create(db=db, obj_in=message_in)
    logger.info(f"Created object with content {created_message.content}")
