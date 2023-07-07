from data_manager import BaseModel
from dataclasses import dataclass

@dataclass
class User(BaseModel):
    TABLE_NAME = 'users'
    COLUMNS = {
        'name':('name','VARCHAR(20)','NOT NULL'),   #      CREATE TABLE users (username VARCHAR(20) UNIQUE,
        'username':('username','VARCHAR(20)','UNIQUE'),  #          name VARCHAR(20) NOT NULL,
        'password':('password','VARCHAR(100)','NOT NULL'),  #      password varchar(100) NOT NULL)
    }

    name: str
    username: str
    password: str


@dataclass
class Message(BaseModel):
    TABLE_NAME = 'messages'
    COLUMNS = {
        'from_user':('from_user','VARCHAR(20)','NOT NULL'), 
        'to_user':('to_user','VARCHAR(20)','NOT NULL'),
        'content':('content','VARCHAR(100)','NOT NULL'),
        'subject':('subject','VARCHAR(100)','NOT NULL'),
        'create_timestamp':('create_timestamp','TIMESTAMP DEFAULT date_trunc(\'second\', now()::timestamp)','NOT NULL'),    }

    from_user: str 
    to_user: str
    content: str
    subject: str
    create_timestamp: str
    