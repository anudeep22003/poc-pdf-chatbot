from sqlalchemy.ext.declarative import as_declarative, declared_attr, declarative_base
from sqlalchemy import Column, Integer
from sqlalchemy.orm import registry

import os

class_registry = registry()

IMPORT_PATH = os.path.abspath(os.path.dirname(__file__))


@class_registry.as_declarative_base()
class Base:
    id = Column(Integer, primary_key=True, autoincrement=True)
    __name__: str

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


if __name__ == "__main__":
    print(dir(Base))
