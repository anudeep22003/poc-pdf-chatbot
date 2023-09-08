from app.crud.crud_base import CRUDBase

# from app.models.message import Message
# from app.schemas.message import MessageCreate
from app import models
from app import schemas
from sqlalchemy.orm import Session


class CRUDMessage(CRUDBase[models.Message, schemas.MessageCreate]):
    def get_messages_by_conv_id(
        self, db: Session, *, conv_id: int
    ) -> list[models.Message]:
        conversation = {"human": [], "agent": []}

        # extract all messages with same conv_id
        return (
            db.query(models.Message)
            .filter(models.Message.conv_id == conv_id)
            .order_by(models.Message.ts_created)
            .all()
        )


message = CRUDMessage(models.Message)
