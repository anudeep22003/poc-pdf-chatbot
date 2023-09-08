import time
from functionality.extract import IndexEventPage, check_if_domain_exists
from functionality.rag_index import BuildRagIndex
from functionality.conversation import UnitConversationManager
from functionality.sitemap import SitemapBuilder
from app import models, schemas, crud, db
from urllib.parse import urlsplit, SplitResult

if __name__ == "__main__":
    split_url = urlsplit("http://www.chinamumbaiexpo.com/")
    i = SitemapBuilder()
    i(split_url)
    # u = UnitConversationManager()
    # u_input = "https://www.autoevexpo.com/"
    # domain = u_input
    # while u_input != "q":
    #     u_input = input(f"Enter a domain, press enter to continue with {domain}  --> ")
    #     if u_input:
    #         domain = u_input
    #     print(f"selected domain: {domain}")
    #     u_input = input("Enter a query: ")
    #     if u_input == "q":
    #         break
    #     query = u_input
    #     query_input = schemas.QueryApiInputBaseClass(domain=domain, query=query)
    #     response = u(query_input=query_input)
    #     print("-" * 20, " Response ", "-" * 20)
    #     print(response.content)
    #     print("-" * 20, " Sources ", "-" * 20)
    #     print(response.sources)
    #     print("-" * 40, "\n")
