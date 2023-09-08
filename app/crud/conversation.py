from app.crud.crud_base import CRUDBase

from app import models
from app import schemas
from sqlalchemy.orm import Session


class CRUDConversation(CRUDBase[models.Conversation, schemas.ConversationCreate]):
    pass


conversation = CRUDConversation(models.Conversation)
