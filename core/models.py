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

    CURRENT_USER = None

    name: str
    username: str
    password: str

    @classmethod
    def login(cls, manager, username, password):
        users = manager.read_all(cls)

        for user in users:
            if user.username == username:
                if user.password == password:
                    return user
                else:
                    return False
        return None


@dataclass
class Message(BaseModel):
    TABLE_NAME = 'message'
    COLUMNS = {
        'sender_id':('sender_id','INT','REFERENCES users(_id)'),   #      CREATE TABLE users (username VARCHAR(20) UNIQUE,
        'reciever_id':('reciever_id','INT','REFERENCES users(_id)'),  #          name VARCHAR(20) NOT NULL,
        'data':('data','VARCHAR(200)','NOT NULL'),  #      password varchar(100) NOT NULL)
        'created_at':('created_at', 'TIMESTAMP', 'DEFAULT NOW()'),
        'draft':('draft', 'BOOLEAN')
    }

    sender_id: int
    reciever_id: int
    data: str
    draft: bool


    # implement send

