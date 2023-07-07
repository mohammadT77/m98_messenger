from data_manager import DBManager
from core.models import User
from menu import models
from core.menu_actions import *
    

main_menu_route = {
    'name':'maktab98 messanger',
    'children': [
        {
            'name': 'Create',
            'action': create
        },
        {
            'name': 'Inbox',
            'action': inbox
        },
        {
            'name': 'Send box',
            'action': sentbox
        },
        {
            'name': 'Drafts',
            'action': draft
        },
        {
            'name': 'Logout',
            'action': logout
        }
    ]
}

main_root_menu = models.generate_menu_from_dict(main_menu_route)


def main():
    try: 
        if login():
            main_root_menu()

    except Exception as e:
        print(e)
        print("Login first")


if __name__ == "__main__":
    main()
