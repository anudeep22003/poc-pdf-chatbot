from functionality.rag_index import BuildRagIndex, QueryRagIndex
from urllib.parse import urlsplit, SplitResult
import pandas as pd

import signal


class timeout:
    def __init__(self, seconds=1, error_message="Timeout"):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)


# open the csv file that contains the domain to index
df = pd.read_csv("data/events_to_index.csv")


def get_domains() -> list[str]:
    return df[df["done"].isna()]["website"].tolist()


for domain in get_domains():
    urlsplit_obj = urlsplit(domain)
    with timeout(seconds=1200):
        try:
            b = QueryRagIndex(urlsplit_obj=urlsplit_obj)
        except TimeoutError:
            print(f"Timeout error for {domain}")
            df.loc[df["website"] == domain, "done"] = "timeout"
            df.to_csv("data/events_to_index.csv", index=False)
            continue
    df.loc[df["website"] == domain, "done"] = "indexed, ready to use"
    df.to_csv("data/events_to_index.csv", index=False)

# url = "http://35.200.180.141:8001/converse-website/"

# ses = requests.Session()
# ses.headers.update({"Content-Type": "application/json"})


# for domain in domains:
#     payload = json.dumps(
#         {
#             "domain": domain,
#             "query": "Give me a brief description of the event in a list form. Generate response in markdown.",
#         }
#     )

#     response = ses.get(url, data=payload)

#     with open("data/initial_index.log", "a") as d:
#         s = domain + "\n" + "-" * 30 + "\n" + response.text + "\n" + "-" * 30 + "\n"
#         d.write(s)
