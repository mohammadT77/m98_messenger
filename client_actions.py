import datetime

from menu.utils import get_input
from data_manager.db_manager import *
from core.models import User, Message
# from data_manager.config import config
"""
CREATE TABLE users (
id SERIAL PRIMARY KEY,
username VARCHAR(50) UNIQUE NOT NULL,
password_hash VARCHAR(128) NOT NULL CHECK (length(password_hash) = 128),
password VARCHAR NOT NULL,
CONSTRAINT valid_password CHECK (password_hash = crypt(password, password_hash))
);
"""
config2 = {'host' :'localhost', 'database':'test_database', 'user':'postgres','password':'MaA98218'}

# my_database_manager = DBManager({'db_config': config('requirements.ini', "postgresql")})
my_database_manager = DBManager({'db_config': config2})


def register():
    name = get_input("Enter your name: ")
    username = get_input("Enter your username: ")
    password = get_input("Enter your password: ")
    user = User(name, username, password)
    user_id = my_database_manager.create(user)
    loaded_user = my_database_manager.read(user_id)
    print("You registration successfully done.")
    return loaded_user


def login():
    username = get_input("Enter your username: ")
    password = get_input("Enter your password: ")
    query = f"SELECT * from users WHERE username = {username};"
    loaded_user = my_database_manager.raw_query(query)[0]
    if loaded_user.password == password:
        print("You logged in successfully.")
        return loaded_user
    print("passw")
    user_choice = get_input("Do you want to register(y/n): ")
    if user_choice.lower() == 'y':
        register()
    login()



def create_message(user: User):
    to_user_username = get_input("who do you want to message (username): ") # TODO
    query = f"SELECT to_user from users WHERE username = {to_user_username};"
    to_user = my_database_manager.raw_query(query)[0]
    print(to_user)

    # to_user = get_input("who do you want to message (id): ", target_type=int)

    # assert
    message = get_input("Enter message: ")
    subject = get_input('Enter subject: ')
    # message_model = Message(user)
    message_model = Message(int(to_user), int(user._id), datetime.datetime.now(), subject, message)
    my_database_manager.create(message_model)
    print("Message Created")


def check_inbox(user: User):
    query = f"SELECT * from messages WHERE to_user = {user._id};"
    messages = my_database_manager.raw_query(query)
    for message in messages:
        print(*message)


def check_sent_box(user: User):

    query = f"SELECT * from messages WHERE from_user = {user._id};"
    messages = my_database_manager.raw_query(query)
    for message in messages:
        print(*message)


