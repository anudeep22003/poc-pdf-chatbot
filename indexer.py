from llama_index import (
    Document,
    VectorStoreIndex,
    get_response_synthesizer,
    StorageContext,
    load_index_from_storage,
)
from llama_index.retrievers import VectorIndexRetriever
from llama_index.node_parser import SimpleNodeParser
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.indices.postprocessor import SimilarityPostprocessor
from llama_index.schema import Node

import unstructured
from unstructured.partition.auto import partition

import os
from collections import defaultdict
from itertools import chain
import logging


SIMILARITY_TOP_K = 5
PATH_RAG_INDEX = "data/rag-index/"
PATH_TO_DATA = "data/"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("indexer.log", mode="a")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

product_descriptions = {
    "CEREC Primemill": "This is an device that is used for computed-aided production of dental restorations, abutments, parts of abutments and drilling templates for implant placement.",
    "Primescan Connect": "Primescan Connect allows you to create digital impressions for detnal purposes and send digital scans to a laboratory of your choice to manufacture at your laboratory partner.",
    "CEREC SW 5": """
    The CEREC SW 5 software is used to create optical impressions of dentulous, partially edentulous or completely edentulous jaw situations. Digital models of the jaw situations are created in CEREC SW 5 based on the optical impressions. The designs can be exported for preparation from dental materials.
    """,
}

index_to_product_mapping = {
    "CEREC Primemill": "IFU_CEREC_Primemill.pdf",
    "Primescan Connect": "IFU_Primescan_Connect.pdf",
    "CEREC SW 5": "OM_CEREC_SW_5.pdf",
}


class BuildRagIndex:
    def __init__(self, doc_filename: str, start_skip: int = 0, end_skip: int = 0):
        self.doc_filename = doc_filename  # IFU_CEREC_Primemill_EN_6719681.pdf
        self.start_skip = start_skip
        self.end_skip = end_skip
        self.rag_index = self.build_or_retrieve_index()
        pass

    def build_or_retrieve_index(self) -> VectorStoreIndex:
        index_exists = self.check_if_index_exists()

        if index_exists:
            # retrieve index
            return self.retrieve_index()
        else:
            logger.debug(
                f"index does not exist for {self.doc_filename}, hence building it."
            )
            # build and retrieve index
            paged_text = self.split_document_into_pages()
            rag_index = self.build_index(paged_text)
            # save rag index
            self.save_rag_index(rag_index)
            return rag_index

    def check_if_index_exists(self) -> bool:
        "use filename to check if index exists"
        index_dir = os.path.join(os.getcwd(), PATH_RAG_INDEX, self.doc_filename)

        logger.debug(f"checking if index exists at {index_dir}")

        dir_exists_on_filesystem = os.path.exists(index_dir)
        logger.debug(f"index exists on filesystem: {dir_exists_on_filesystem}")
        return dir_exists_on_filesystem

    def retrieve_index(self) -> VectorStoreIndex:
        "called if check index comes true"
        sc = StorageContext.from_defaults(
            persist_dir=os.path.join(os.getcwd(), PATH_RAG_INDEX, self.doc_filename)
        )
        index = load_index_from_storage(sc)
        #! make sure you are ok with removing index_id
        return index

    def split_document_into_pages(self) -> dict:
        """
        take a pdf document and split it into paged content
        - skip pages at the start to account for table of content and other cruft
        - skip end to account for ending cruft

        Output:
        - a dict of {page_number: text}
        """
        document_location = os.path.join(os.getcwd(), PATH_TO_DATA, self.doc_filename)
        logger.debug(
            f"document to be indexed checked for at location: {document_location}"
        )

        elements = partition(filename=document_location)
        paged_text_list = defaultdict(list)
        logger.debug(f"paged_text_list {list(paged_text_list.items())[25:35]}")
        for el in elements:
            paged_text_list[el.metadata.page_number].append(el.text)

        length_of_paged_text_list = len(paged_text_list)
        skipped_pages = list(
            chain(
                range(self.start_skip),
                range(
                    length_of_paged_text_list - self.end_skip, length_of_paged_text_list
                ),
            )
        )
        logger.debug(f"skipped_pages {skipped_pages}")

        paged_text = {
            pagenumber: "\n".join(textlist)
            for pagenumber, textlist in paged_text_list.items()
            if pagenumber not in skipped_pages
        }

        logger.debug(f"paged_text: {list(paged_text.items())[25:35]}")

        return paged_text

    def build_index(self, paged_document: dict):
        """
        index document and store it with the filename
        """
        parser = SimpleNodeParser.from_defaults()

        documents = [
            Document(doc_id=pagenum, text=text_on_page)
            for pagenum, text_on_page in paged_document.items()
        ]
        logger.debug("num of documents created {}".format(len(documents)))
        nodes = parser.get_nodes_from_documents(documents, show_progress=True)
        logger.debug("num of nodes created {}".format(len(nodes)))
        rag_index = VectorStoreIndex(nodes)
        self.save_rag_index(rag_index)
        return rag_index

        ...

    def save_index_with_filename(self):
        "save the index with the filename"
        ...

    def save_rag_index(self, rag_index: VectorStoreIndex):
        "save the rag index to the disk"
        "store in directory, if directory does not exist create it"
        dir_to_save_index = os.path.join(os.getcwd(), PATH_RAG_INDEX, self.doc_filename)
        if not os.path.exists(dir_to_save_index):
            os.makedirs(dir_to_save_index)
        # rag_index.set_index_id(self.urlsplit_obj.netloc)
        rag_index.storage_context.persist(persist_dir=dir_to_save_index)

    def query(self, query_text: str):
        response = self.query_rag_index(query_text)
        response_text = str(response)
        sources = set(
            [
                node_with_score.node.ref_doc_id
                for node_with_score in response.source_nodes
            ]
        )
        logger.debug(f"response from query: {response_text}\n\nsources: {sources}")
        return response_text, sources

    def query_rag_index(self, query_text: str):
        "query the index for a given query"
        logger.debug(f"querying rag index for --> {query_text}")
        retriever = VectorIndexRetriever(
            index=self.rag_index,
            similarity_top_k=10,
            # node_ids=node_ids,
            # filters=keyword_filters,
        )

        # level 1 retreival
        retrieved_nodes = retriever.retrieve(query_text)
        logger.debug(
            f"number of retrieved_nodes after 1st retreival: {len(retrieved_nodes)}"
        )

        def get_pages(retrieved_nodes: list[Node]) -> list[str]:
            return [
                (node_with_score.node.ref_doc_id, node_with_score.score)
                for node_with_score in retrieved_nodes
            ]

        # print(retrieved_nodes[:2])
        logger.debug(f"page_nums: {get_pages(retrieved_nodes)}")
        # level 2 retreival
        retriever = VectorIndexRetriever(
            index=self.rag_index,
            node_ids=[node.node_id for node in retrieved_nodes],
            similarity_top_k=2,
        )

        retrieved_nodes = retriever.retrieve(query_text)
        logger.debug(
            f"number of retrieved_nodes after 2nd retreival: {len(retrieved_nodes)}"
        )
        logger.debug(f"page_nums: {get_pages(retrieved_nodes)}")

        # # configure response synthesizer
        # response_synthesizer = get_response_synthesizer()

        # construct index to query using retreived nodes
        query_index = VectorStoreIndex(
            nodes=[node_with_score.node for node_with_score in retrieved_nodes]
        )

        # assemble query engine
        query_engine = query_index.as_query_engine(
            # streaming=True
        )

        response = query_engine.query(query_text)
        return response


if __name__ == "__main__":
    b = BuildRagIndex("IFU_CEREC_Primemill.pdf", start_skip=4, end_skip=6)
    b.query("What is CEREC Primemill?")
