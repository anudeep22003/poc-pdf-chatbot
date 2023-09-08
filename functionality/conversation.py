from app import models, schemas, crud, db
from app.schemas.custom_classes import QueryApiInputBaseClass
from typing import Optional
from app.deps import get_db
from functionality.extract import check_if_domain_exists, IndexEventPage
from functionality.rag_index import QueryRagIndex
import logging
import time
from urllib.parse import urlsplit, SplitResult

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler(f"logs/{__name__}.log", mode="a")
fh.setLevel(logging.INFO)
logger.addHandler(fh)


class UnitConversationManager:
    """A manager class to handle conversations
    Responsibilities:
    - generate a new conversation id and log to db
    - query the rag_index
    - log query and response to db
    - return the message model of the response
    """

    def __init__(self) -> None:
        pass

    def get_new_conv_id(self, urlsplit_obj: SplitResult) -> int:
        "generate a conversation id"
        new_conv = schemas.ConversationCreate(domain=urlsplit_obj.netloc)

        with get_db() as db:
            conv = crud.conversation.create(db=db, obj_in=new_conv)
        return conv.id

    def store_message_in_db(self, message: schemas.Message) -> None:
        "store message in database"
        with get_db() as db:
            msg_obj = crud.message.create(db=db, obj_in=message)
        return msg_obj

    def __call__(self, query_input: QueryApiInputBaseClass) -> models.Message:
        # track time for response
        start_time = time.perf_counter()

        "generate a response based on domain and query"
        urlsplit_obj = urlsplit(query_input.domain)
        query = query_input.query
        # create new conversation id
        conv_id = self.get_new_conv_id(urlsplit_obj=urlsplit_obj)
        q = QueryRagIndex(urlsplit_obj=urlsplit_obj)
        response_object = q.query_index(query_text=query)

        query_db_obj = schemas.MessageCreate(
            conv_id=conv_id,
            content=query,
            sender="human",
            receiver="system",
        )
        query_from_db = self.store_message_in_db(message=query_db_obj)
        response_db_object = schemas.MessageCreate(
            conv_id=conv_id,
            content=str(response_object),
            sender="system",
            receiver="human",
            sources=",\n".join(
                set(
                    [
                        node_with_score.node.ref_doc_id
                        for node_with_score in response_object.source_nodes
                    ]
                )
            ),
            response_time=round(time.perf_counter() - start_time, 2),
        )
        response_from_db = self.store_message_in_db(message=response_db_object)
        logger.info(f"query from db: {query}")
        logger.info(f"response from db: {response_object}")
        logger.info(response_object.source_nodes)
        #! do you need to reconstruct this to keep input and output api obj same?
        return response_from_db
