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
    pass
