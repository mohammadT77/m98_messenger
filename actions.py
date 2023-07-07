from data_manager.db_manager import DBManager
from menu.utils import get_input
from core.models import Message, User


# def login():
#     username = get_input("Enter user name")

db_config = {
    'dbname':'test', 'host':'localhost',
     'password':'postgres', 'user':'postgres', 'port': '5432'
     }
    

manager = DBManager({'db_config':db_config})


def signup():
    name = get_input("Enter name: ")
    username = get_input("Enter username: ")
    password = get_input("Enter password: ")

    user = User(name, username, password)

    manager.create(user)


def login():
    ch = get_input("1. Login\n2. signup\n>>>")
    if ch == '2':
        signup()
        return login()
    
    username = get_input("Enter username: ")
    password = get_input("Enter password: ")

    users = manager.read_all(User)

    for user in users:
        if user.username == username:
            if user.password == password:
                global userid
                userid = user._id
                return userid
            else:
                print("wrong password try again!")
                return login()
            
    print("username does not exists!")
    return login()


def create():
    reciever_username = get_input("Enter reciever username: ")
    data = get_input("Enter data: ")
    draft = get_input("would you like to send this message?(True/False): ")
    
    for user in manager.read_all(User):
        if user.username == reciever_username:
            reciever_id = user._id

    message = Message(userid, reciever_id, data, draft)

    manager.create(message)


def send(m:object):
    m.draft = True
    manager.update(m)

def draft():
    messages = manager.read_all(Message)

    inbox = []
    for _m in messages:
        if _m.sender_id == userid and not bool(_m.draft):
            inbox.append(_m)
    
    if not inbox:
        print("no messages yet!")
    else:
        for i, m in enumerate(inbox):
            print(f"{i+1}. {m.data}\n{m.created_at}")

    choice = get_input("Enter message number to send(leave empty to return)")

    if choice and choice.isdigit():
        idx = int(choice) -1
        obj = inbox[idx]

        return send(obj)

def inbox():
    messages = manager.read_all(Message)

    inbox = []
    for _m in messages:
        if _m.reciever_id == userid:
            inbox.append(_m)
    
    if not inbox:
        print("no messages yet!")
    else:
        for i, m in enumerate(inbox):
            print(f"{i+1}. {m.data}\n{m.created_at}")
    

def sent():
    messages = manager.read_all(Message)

    inbox = []
    for _m in messages:
        if _m.sender_id == userid and bool(_m.draft):
            inbox.append(_m)
    
    if not inbox:
        print("no sent messages yet!")
    else:
        for i, m in enumerate(inbox):
            print(f"{i+1}. {m.data}\n{m.created_at}")


def logout():
    return login()


