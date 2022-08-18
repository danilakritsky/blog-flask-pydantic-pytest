
import os
import sqlite3
import uuid

from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr, Field




class Article(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    author: EmailStr
    title: str
    content: str

    @classmethod
    def get_by_id(cls, id: str):
        # not using the context manager since it just commits, 
        # and does note close the connection
        con: sqlite3.Connection = sqlite3.connect(os.getenv('DB_PATH', ':memory:'))
        cur: sqlite3.Cursor = con.cursor()
        res: sqlite3.Cursor = cur.execute('SELECT * FROM articles WHERE id = ?', (id,))
        article: Article = cls(**res.fetchone())
        return article