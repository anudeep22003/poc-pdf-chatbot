from app import models
from app.crud.message import message
from sqlalchemy.orm import Session
from app import schemas
from functionality.ai_models import chat_client
import langchain.llms
from llama_index import Prompt

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler(f"logs/{__name__}.log")
fh.setLevel(logging.INFO)
logger.addHandler(fh)


class ConversationManager:
    def __init__(self, llm_client: langchain.llms) -> None:
        self.client = llm_client
        self.context = None
        self.conv_id = None
        self.db = None

    #######################################################
    #########        LLM response generator       #########
    #######################################################

    def __call__(self, input_msg: schemas.Message, db: Session) -> str:
        # ensure msg comes from human
        assert input_msg.sender == "human", f"invalid sender {input_msg.sender}"

        # construct context,
        self.conversation_context_initializer(conv_id=input_msg.conv_id, db=db)
        # construct context string to insert into prompt
        composed_context_string = self.context_string_constructor(
            incoming_msg=input_msg
        )
        return self.client(composed_context_string)

    def check_if_conv_id_changed(self, conv_id: int) -> bool:
        if (self.conv_id != conv_id) or (self.conv_id is None):
            return True
        else:
            return False

    def get_system_prompt(self) -> str:
        return """You are an agent trained to assist humans in a conversational form. Use the context of the human's and your own responses above to best answer the below query as an agent. Use only the context information without relying on prior knowledge. Respond in markdown format.\nIf you are unable to answer using the given context, respond with "The organizer does not seem to have shared this information. Try visiting the website yourself." \n\nAnswer the following question: {query_str}\n"""

    #######################################################
    ######### conversation context initialization #########
    #######################################################

    def conversation_context_initializer(self, conv_id: int, db: Session):
        if self.check_if_conv_id_changed:
            # set new conv_id
            self.conv_id = conv_id
            # initialize empty context
            self.context = self.initialize_context()
            # crud, read data from database and get all messages of conv_id
            all_conv_msg = self.extract_conv_msg_from_sql(conv_id, db)
            # construct into context
            self.append_to_context(all_conv_msg)

    def initialize_context(self):
        return {"human": [], "agent": []}

    def extract_conv_msg_from_sql(
        self,
        conv_id: int,
        db: Session,
    ) -> list[models.Message]:
        return message.get_messages_by_conv_id(db=db, conv_id=conv_id)

    def append_to_context(self, input_msgs: list[models.Message]):
        for msg in input_msgs:
            try:
                self.context[msg.sender].append(msg.content)
            except KeyError:
                print(f"Key error, key {msg.sender} not found.")

    def context_string_constructor(self, incoming_msg: schemas.Message) -> list[str]:
        combined_context = zip(*self.context.values())

        # converts lengths to set to ensure sizes of human and agent context is same
        assert set(
            [len(item) for item in self.context.values()]
        ), "different context lengths"

        context_msg_list = [
            f"human:\n{human_response}\nagent:{agent_response}"
            for human_response, agent_response in combined_context
        ]
        # add the system / instruction prompt
        context_msg_list.append(self.get_system_prompt())
        # add the input message to context msg list
        context_msg_list.append(f"human:\n{incoming_msg.content}\nagent:\n")

        combined_context_string = "\n".join(context_msg_list)

        logger.info(f"{'-'*30}\n{combined_context_string}\n\n")
        #! changed this to be a prompt of the type llama index likes, change later if nec
        return Prompt(combined_context_string)


converser = ConversationManager(chat_client)
