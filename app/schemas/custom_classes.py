from pydantic import BaseModel


class QueryApiInputBaseClass(BaseModel):
    domain: str
    query: str
