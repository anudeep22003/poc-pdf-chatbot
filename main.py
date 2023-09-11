from langchain.llms import OpenAI
from agents import Agent, classification_agent
from indexer import BuildRagIndex, index_to_product_mapping, product_descriptions

from fastapi import FastAPI
from pydantic import BaseModel, Field
import json

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler("query.log", mode="a")
fh.setLevel(logging.INFO)
logger.addHandler(fh)


class Message(BaseModel):
    content: str
    # role: str = Field(description="agent | human (role of the actor sending the message)")


class Response(BaseModel):
    response: str
    product: str | None
    sources: str | None


app = FastAPI()


query = "What are the most important maintenance steps I need to do within one year?"
query = "Something is wrong with the scanner. What should I do?"


memory_conv_id = 0

global_memory: Message | None = None


def memory_refresher():
    with open("memory.txt", "w") as f:
        f.write("None")


def memory_getter() -> Message | None:
    f = open("memory.txt", "r")
    memory = f.read()
    f.close()
    if memory == "None":
        # return ready to restart
        return None
    else:
        memory = json.loads(memory)
        return Response(**memory)


@app.get("/converse/")
def get_response(
    message: Message,
) -> dict | Response:
    logger.info(message.content)

    # attempt at adding memory did not succeed, no confirmation possible for now from user
    # memory = memory_getter()

    # if memory is None:
    #     print("memory is None, hence doing classification")
    #     # means this is a fresh request
    #     # send a classification response
    #     return get_classification(message)
    #     ...
    # elif message.content.lower() in ["", "y", "yes"]:
    #     # switch the message so as to reset the memory for the next call
    #     memory_refresher()
    #     # perform the rag call
    #     return perform_rag_call(memory)

    # def get_classification(message: Message) -> Response:

    # product_that_query_is_about = classification_agent(message.content)
    # product_that_query_is_about = product_that_query_is_about.strip()

    # logger.debug(f"product_that_query_is_about: {product_that_query_is_about}")
    # # appropriate rag index
    # try:
    #     index_id = index_to_product_mapping[product_that_query_is_about]
    #     msg1 = f"You seem to be asking about {product_that_query_is_about}.\n\nIf it isn't, try asking the question again with a few more contextual clues.\nI am fairly capable, and I'll figure it out for you."
    #     return Response(
    #         response=msg1, product=product_that_query_is_about, sources=None
    #     )
    # except KeyError:
    #     msg1 = f"Sorry, I cannot seem to find the product you are asking about in my database.\n\n"
    #     msg2 = f"As reference, I only have the following products in my database:\n{list(index_to_product_mapping.keys())}"
    #     msg3 = f"\n\nPlease try again. It may help to give any identifying infromation about the product for my benefit."
    #     # return Response(response=msg1 + msg2 + msg3, product=None, sources=None)

    # # def perform_rag_call(message: Message) -> Response:
    # response query initialize
    response_query = []
    # find the appropriate index for the product
    product_that_query_is_about = classification_agent(message.content)
    product_that_query_is_about = product_that_query_is_about.strip()

    print(f"product_that_query_is_about: {product_that_query_is_about}")
    # appropriate rag index
    try:
        index_id = index_to_product_mapping[product_that_query_is_about]
        msg1 = f"You seem to be asking about {product_that_query_is_about}."
    except KeyError:
        msg1 = f"Sorry, I cannot seem to find the product you are asking about in my database."
        msg2 = f"I only have the following products in my database: {list(index_to_product_mapping.keys())}"
        msg3 = f"Please try again. It may help to give any identifying infromation about the product for my lookup benefit."
        response_query.extend([msg1, msg2, msg3])
        response_obj = {
            "response": "\n\n".join(response_query),
            "product": None,
            "sources": None,
        }
        logger.info(response_obj)
        logger.info(f"\n {'-'*30}\n")
        return response_obj
        ...

    b = BuildRagIndex(index_id)
    response_text, page_numbers = b.query(message.content)
    response_query.append(msg1)
    response_query.append(response_text)
    response_obj = {
        "response": "\n\n".join(response_query),
        "product": product_that_query_is_about,
        "sources": ", ".join(page_numbers),
    }
    logger.info(response_obj)
    logger.info(f"\n {'-'*30}\n")
    return response_obj


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
    # while True:
    #     query = input("Enter query: ")
    #     print(get_response(Query(query=query)))
