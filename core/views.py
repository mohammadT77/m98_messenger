from core.utils import *
from core.models import User, Message
from data_manager import DBManager
from db_config import db_config
import json
    

manager = DBManager({'db_config':db_config})


def get_user(req: Request) -> Response:
    username = req.headers.get('USERNAME')
    password = req.headers.get('PASSWORD')

    current_user = User.login(manager, username, password)
    if not current_user:
        return Response(b"User is not authenticated", 403, 'text/plain')
    
    return Response(json.dumps(current_user.to_dict()).encode(), 200)


def change_name(req: Request) -> Response:
    # TODO: modify user name using json.loads(req.body)['name']
    return Response(b'TODO', 500, 'text/plain')

def register_user(req: Request) -> Response:
    # TODO: create new user by json.loads(req.body) data
    return Response(b'TODO', 500, 'text/plain')

def create_message(req: Request):
    username = req.headers.get('USERNAME')
    password = req.headers.get('PASSWORD')

    current_user = User.login(manager, username, password)
    if not current_user:
        return Response(b"User is not authenticated", 403, 'text/plain')
    
    # {"to_user":"@asqar", "content":"Hello asqar"}
    msg_data = json.loads(req.body.decode())
    
    # Get message data from req.body
    receiver_username = msg_data.get('to_user', None)
    msg_content = msg_data.get('content', None)

    # Check if required data is provided
    if not receiver_username:
        return Response(b"Enter `to_user` username", 400, 'text/plain')
    if not msg_content:
        return Response(b"Enter message `content`", 400, 'text/plain')

    sender = current_user
    for _user in manager.read_all(User):
        _user: User
        if _user.username == receiver_username:
            receiver = _user
            break
    else:
        return Response(b"Receiver user not found", 404, 'text/plain')
    
    message = Message(sender._id, receiver._id, msg_content, False)

    manager.create(message)

    message_json = json.dumps({'message':message.to_dict()})

    return Response(message_json.encode(), 200)


def inbox(req: Request):
    username = req.headers.get('USERNAME')
    password = req.headers.get('PASSWORD')

    current_user = User.login(manager, username, password)
    if not current_user:
        return Response(b"User is not authenticated", 403, 'text/plain')
    
    def map_messages_dict(msg):
        msg.created_at = str(msg.created_at)
        return msg.to_dict()
    
    all_messages = manager.read_all(Message)
    messages_received = filter(lambda msg: msg.reciever_id == current_user._id, all_messages)
    messages_dict = map(map_messages_dict, messages_received)
    messages_json = json.dumps({'messages':list(messages_dict)})
    
    return Response(messages_json.encode(), 200)


def sentbox(req: Request) -> Response:
    # TODO: return all sent messages by user
    return Response(b'TODO', 500, 'text/plain')