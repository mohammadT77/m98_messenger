from menu import models, utils

from menu.models import generate_menu_from_dict
from core.models import User, Message
from client_actions import *


def dashboard_menu_creator(user: User):
    dashboard_menu = {
        'name': 'Dashboard',
        'children': [
            {
                'name': 'Create message',
                'action': [create_message],
                'action_parameters': [[user],]

            },
            {
                'name': 'Inbox',
                'action': [check_inbox],
                'action_parameters': [[user], ]

            },
            {
                'name': 'Sent Box',
                'action': [check_sent_box],
                'action_parameters': [[user], ]

            },

        ]
    }
    return generate_menu_from_dict(dashboard_menu)


main_menu_route = {
    'name': 'Login page',
    'children': [
        {
            'name': 'register',
            'action': [register, dashboard_menu_creator],
            'action_parameters': [(), ['res0']]
        },
        {
            'name': 'Login',
            'action': [login, dashboard_menu_creator],
            'action_parameters': [(), ['res0']],

        },

    ]
}


root_menu = generate_menu_from_dict(main_menu_route)



def main():
    root_menu()

main()