# db.py
import os
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, Text
from sqlalchemy.sql import select
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "finance_chat.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
metadata = MetaData()

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("user_type", String)
)

budgets = Table(
    "budgets", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("data", Text)  # store JSON string of budget
)

chats = Table(
    "chats", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("role", String),  # user/assistant
    Column("message", Text)
)

metadata.create_all(engine)

def save_user(name: str, user_type: str) -> int:
    with engine.connect() as conn:
        ins = users.insert().values(name=name, user_type=user_type)
        res = conn.execute(ins)
        return res.inserted_primary_key[0]

def save_budget(user_id: int, data: str) -> int:
    with engine.connect() as conn:
        res = conn.execute(budgets.insert().values(user_id=user_id, data=data))
        return res.inserted_primary_key[0]

def save_chat(user_id: int, role: str, message: str) -> int:
    with engine.connect() as conn:
        res = conn.execute(chats.insert().values(user_id=user_id, role=role, message=message))
        return res.inserted_primary_key[0]

def get_user(user_id: int):
    with engine.connect() as conn:
        s = select(users).where(users.c.id == user_id)
        r = conn.execute(s).fetchone()
        return dict(r) if r else None
