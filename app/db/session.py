from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQL_DATABASE_URL = "sqlite+pysqlite:///conversations.db"

engine = create_engine(
    url=SQL_DATABASE_URL, echo=True, future=True, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)