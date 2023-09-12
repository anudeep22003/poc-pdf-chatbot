from langchain.llms import OpenAI
from agents import Agent, classification_agent
from indexer import BuildRagIndex, index_to_product_mapping, product_descriptions

from flask import Flask, make_response, jsonify
from flask import request
import json
from flask_cors import CORS

from pydantic import BaseModel

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler("query.log", mode="a")
fh.setLevel(logging.INFO)
logger.addHandler(fh)


class Query(BaseModel):
    query: str


class Response(BaseModel):
    response: str
    product: str
    sources: str





query = "What are the most important maintenance steps I need to do within one year?"
query = "Something is wrong with the scanner. What should I do?"

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

@app.route('/chat', methods=['POST', 'OPTIONS'])
def get_response() -> dict:
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    else:
        postData = json.loads(request.data)
        query = postData['query']
        # response query initialize
        response_query = []
        # find the appropriate index for the product
        product_that_query_is_about = classification_agent(query)
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
        response_text, page_numbers = b.query(query)
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
    app.run(host= '0.0.0.0', port=8001)
