from gc import get_debug
import os
import sqlite3
import uuid

from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr, Field
from functools import wraps

load_dotenv()



class Article(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    author: EmailStr
    title: str
    content: str

    @staticmethod
    def ensure_table(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            Article.create_table()
            return func(*args, **kwargs)
        return wrapper


    @classmethod
    @ensure_table
    def get_by_id(cls, id: str) -> 'Article':
        # not using the context manager since it just commits the transaction,
        # and does note close the connection
        con: sqlite3.Connection = sqlite3.connect(Article.get_db())
        cur: sqlite3.Cursor = con.cursor()
        res: sqlite3.Cursor = cur.execute(
            "SELECT * FROM articles WHERE id = ?", (id,)
        )

        article: Article = cls(**res.fetchone())
        con.close()  # !!! close the connection
        return article

    # classmethod should be preferred over staticmethod
    # if the class is expected to be inherited
    # https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner
    
    @staticmethod
    def create_table() -> None:
        con: sqlite3.Connection = sqlite3.connect(
            Article.get_db()
        )
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS
            articles(id TEXT, author TEXT, title TEXT, content TEXT)
            """
        )
        if os.getenv("RUN_ENV") != "TEST":
            con.close()  # don't close for inmemory db

    @staticmethod
    def get_db() -> str:
        db: str
        if os.getenv("RUN_ENV") == "TEST":
            db = os.getenv("TEST_DB_PATH") or ":memory:"
        else:
            db = os.getenv("DB_PATH") or "database.db"
        return db




