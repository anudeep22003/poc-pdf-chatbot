from typing import Generator

from .db.session import SessionLocal
from contextlib import contextmanager


@contextmanager
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    # db = get_db()
    ...
