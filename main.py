from data_manager import DBManager, MessageManager
from core.models import User, Message
from menu.utils import get_input
from menu.models import generate_menu_from_dict
from actions.message_action import *

db_config = {
    'dbname':'m98_second_project',
    'host':'localhost',
    'user':'postgres',
    'password':'Behnam.2201'
}

dbmanager = DBManager({'db_config':db_config})

data = {
        'from_user':'',
        'to_user':'',
        'content':'',
        'subject':'',
        'dbmanager':dbmanager
    }

msgmanager = MessageManager({"msg_config":data})


# print("All users:", *manager.read_all(User), sep='\n')

# print(manager.read(2,User))

# manager.create_table(User)

# u1 = User("jojo","@jotaro","nononoyesyesyes!")
# manager.create(u1)

# uu = User("babak","@hooloo","5564hgfgfsz")
# manager.update(2,uu)

# manager.truncate(User)


main_menu_dict = {
    'name':'Messenger project',
    'children':[
        {
            'name':'Create message',
            'action': create_message,       
        },
        {
            'name':'Inbox',
            'action': inbox_message,
        },
        {
            'name': 'Sent box',
            'action': sentbox_message,
        }
    ]
}

root_menu = generate_menu_from_dict(main_menu_dict, parent=None)


def user_main():
    print("User Login")
    print("----------------")
    username = input("Username: ")
    password = input("Password: ")

    
    login = DBManager.login(dbmanager, username, password, User)
    if login:
        print("Welcome...\n")
        root_menu()
    else:
        print("User does not exist")


if __name__=="__main__":
    user_main()
    # for user in manager.read_all(User):
    #     print(user)