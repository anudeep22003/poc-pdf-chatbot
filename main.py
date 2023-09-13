from langchain.llms import OpenAI
from agents import Agent, classification_agent
from indexer import BuildRagIndex, index_to_product_mapping, product_descriptions

from fastapi import FastAPI
from pydantic import BaseModel, Field
import json

from utils import documents_to_index

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler("query.log", mode="a")
fh.setLevel(logging.INFO)
logger.addHandler(fh)

###### Pydantic base classes for FastAPI ######


class Message(BaseModel):
    content: str


class Response(BaseModel):
    content: str
    product: str | None
    sources: str | None


####################################################


app = FastAPI()


# query = "What are the most important maintenance steps I need to do within one year?"
# query = "Something is wrong with the scanner. What should I do?"


def memory_refresher():
    f = open("memory.txt", "w")
    f.close()


def memory_getter() -> Message | None:
    f = open("memory.txt", "r")
    memory = f.read()
    f.close()
    if memory == "":
        # return means this is a new request
        return None
    else:
        memory = json.loads(memory)
        return Message(**memory)


def memory_writer(memory: Message):
    with open("memory.txt", "w") as f:
        f.write(json.dumps(memory.dict()))


def get_classification(message: Message) -> Response:
    product_that_query_is_about = classification_agent(message.content)
    product_that_query_is_about = product_that_query_is_about.strip()

    logger.debug(f"product_that_query_is_about: {product_that_query_is_about}")
    # appropriate rag index
    try:
        index_id = index_to_product_mapping[product_that_query_is_about]
        msg1 = f"You seem to be asking about {product_that_query_is_about}. Press enter if I got it right. \n\nIf not type `no`, and I will try asking the question again.\n\nI am fairly capable, so help me with a few contextual clues and I'll figure it out."
        return Response(content=msg1, product=product_that_query_is_about, sources=None)
    except KeyError:
        msg1 = f"Sorry, I cannot seem to find the product you are asking about in my database.\n\n"
        msg2 = f"As reference, I only have the following products in my database:\n{list(index_to_product_mapping.keys())}"
        msg3 = f"\n\nPlease try again. It may help to give any identifying information about the product for my benefit."
        return Response(content=f"{msg1}{msg2}{msg3}", product=None, sources=None)


def perform_rag_call(message: Message) -> Response:
    # response query initialize
    response_query = []
    # find the appropriate index for the product
    product_that_query_is_about = classification_agent(message.content)
    product_that_query_is_about = product_that_query_is_about.strip()

    print(f"product_that_query_is_about: {product_that_query_is_about}")
    # appropriate rag index
    try:
        index_id = index_to_product_mapping[product_that_query_is_about]
        msg1 = f"Product: {product_that_query_is_about}.\n\n"
    except KeyError:
        msg1 = f"Sorry, I cannot seem to find the product you are asking about in my database."
        msg2 = f"I only have the following products in my database: {list(index_to_product_mapping.keys())}"
        msg3 = f"Please try again. It may help to give any identifying infromation about the product for my lookup benefit."
        response_query.extend([msg1, msg2, msg3])
        response_obj = {
            "content": "\n\n".join(response_query),
            "product": None,
            "sources": None,
        }
        logger.info(response_obj)
        logger.info(f"\n {'-'*30}\n")
        return Response(**response_obj)

    b = BuildRagIndex(index_id)
    response_text, page_numbers = b.query(message.content)
    # sort page numbers for presentation
    page_numbers = sorted(page_numbers)
    response_query.append(msg1)
    response_query.append(response_text)
    response_obj = {
        "content": "\n\n".join(response_query),
        "product": product_that_query_is_about,
        "sources": ", ".join([str(page_num) for page_num in page_numbers]),
    }
    logger.info(response_obj)
    logger.info(f"\n {'-'*30}\n")
    return Response(**response_obj)


@app.post("/converse/")
def get_response(
    message: Message,
) -> Response | dict:
    logger.info(message.content)

    memory = memory_getter()

    # one more check for if memory is a prev memory
    # this can be done by checking if memory has the message content in its string.

    #

    if memory is None:
        print("memory is None, hence doing classification")
        # means this is a fresh request
        # send a classification response
        memory_writer(message)
        response_msg = get_classification(message)
        if "sorry" in response_msg.content.lower():
            memory_refresher()
            return response_msg
        return response_msg
    elif message.content.strip().lower() in ["n", "no"]:
        memory_refresher()
        return Response(
            content="Sorry for getting it wrong, request you to try asking your question again.\nYou can ask the same question again with a few more contextual clues.\n",
            product=None,
            sources=None,
        )
    elif message.content.strip().lower() in ["", "y", "yes"]:
        # switch the message so as to reset the memory for the next call
        memory_refresher()
        # perform the rag call
        return perform_rag_call(memory)
    else:
        memory_refresher()
        return Response(
            content="Apologoes for the hiccup. Needed to reset my memory there. Now, I am ready. Please ask me again.",
            product=None,
            sources=None,
        )


class ConversationHandler:
    def __init__(self, message: Message):
        self.memory: Message | None = None


if __name__ == "__main__":
    # memory_refresher()
    # import uvicorn

    # uvicorn.run(app, port=8001)

    # for doc_location, start_skip, end_skip in documents_to_index:
    #     BuildRagIndex(doc_location, start_skip, end_skip)
    while True:
        query = input("Enter query: ")
        message = Message(content=query)
        print(get_response(message))
