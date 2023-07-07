import datetime

from data_manager.base import BaseModel
from dataclasses import dataclass


@dataclass
class User(BaseModel):
    TABLE_NAME = 'users'
    COLUMNS = {
        'name': ('name', 'VARCHAR(20)', 'NOT NULL'),  # CREATE TABLE users (username VARCHAR(20) UNIQUE,
        'username': ('username', 'VARCHAR(20)', 'UNIQUE'),  # name VARCHAR(20) NOT NULL,
        'password': ('password', 'VARCHAR(100)', 'NOT NULL',),  # password varchar(100) NOT NULL)
    }

    name: str
    username: str
    password: str


@dataclass
class Message(BaseModel):
    TABLE_NAME = 'messages'
    COLUMNS = {
        'to_user': ('to_user', 'INT', f'REFERENCES {User.TABLE_NAME} (_id)', 'NOT NULL'),
        'from_user': ('from_user', 'INT', f'REFERENCES {User.TABLE_NAME} (_id)', 'NOT NULL'),
        'create_date': ('create_date', 'VARCHAR(100)', 'NOT NULL',),
        'subject': ('subject', 'VARCHAR(100)', 'NOT NULL',),
        'content': ('content', 'VARCHAR(100)', 'NOT NULL',),
        'is_seen': ('is_seen', 'BOOLEAN',),
    }

    to_user: int
    from_user: int
    create_date: datetime.datetime
    subject: str
    content: str
    is_seen: bool = False
