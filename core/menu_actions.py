from data_manager.db_manager import DBManager
from menu.utils import get_input
from core.models import Message, User
from db_config import db_config    

manager = DBManager({'db_config':db_config})


def signup():
    print("Register:")
    name = get_input("Enter name: ")
    username = get_input("Enter username: ")
    password = get_input("Enter password: ")

    user = User(name, username, password)

    manager.create(user)
    
    User.CURRENT_USER = user
    
    return user


def login():
    
    username = get_input("Enter username: ")
    password = get_input("Enter password: ")

    user = User.login(manager, username, password)
    User.CURRENT_USER = user
    
    if user is None:
        print("username does not exist!")
        return signup()
    elif user is False:
        print("invalid password, try again:")
        return login()
    else:
        print("Welcome")
        return user
    


def create():
    receiver_username = get_input("Enter receiver username: ")
    data = get_input("Enter text: ")
    draft = get_input("would you like to send this message?(True/False): ")
    

    sender = User.CURRENT_USER

    for user in manager.read_all(User):
        user: User
        if user.username == receiver_username:
            receiver = user
            break
    else:
        print("Receiver user not found")
        return
    
    message = Message(sender._id, receiver._id, data, draft)

    manager.create(message)
    print("Message created!")


def send(m:object):
    m.draft = True
    manager.update(m)

def draft():
    messages = manager.read_all(Message)

    inbox = []
    for _m in messages:
        if _m.sender_id == User.CURRENT_USER and not bool(_m.draft):
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
        if _m.reciever_id == User.CURRENT_USER._id:
            inbox.append(_m)
    
    if not inbox:
        print("no messages yet!")
    else:
        for i, m in enumerate(inbox):
            print(f"{i+1}. {m.data}\n{m.created_at}")
    

def sentbox():
    messages = manager.read_all(Message)

    inbox = []
    for _m in messages:
        if _m.sender_id == User.CURRENT_USER._id and bool(_m.draft):
            inbox.append(_m)
    
    if not inbox:
        print("no sent messages yet!")
    else:
        for i, m in enumerate(inbox):
            print(f"{i+1}. {m.data}\n{m.created_at}")


def logout():
    return login()


