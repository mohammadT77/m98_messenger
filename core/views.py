from core.utils import *
from core.models import User, Message
from data_manager import DBManager
from db_config import db_config
import json
    

manager = DBManager({'db_config':db_config})


def create_message(req: Request):
    username = req.headers.get('USERNAME')
    password = req.headers.get('PASSWORD')

    current_user = User.login(manager, username, password)
    if not current_user:
        return Response(b"User is not authenticated", 403, 'text/plain')
    
    # {"to_user":"@asqar", "content":"Hello asqar"}
    msg_data = json.loads(req.body.decode())
    assert 'to_user' in msg_data
    assert 'content' in msg_data

    sender = current_user
    for _user in manager.read_all(User):
        _user: User
        if _user.username == msg_data['to_user']:
            receiver = _user
            break
    else:
        return Response(b"Receiver user not found", 404, 'text/plain')
    
    message = Message(sender._id, receiver._id, msg_data['content'], False)

    manager.create(message)
    return Response(b'{"msg":"Your message is created"}', 200)

def inbox(req: Request):
    username = req.headers.get('USERNAME')
    password = req.headers.get('PASSWORD')

    current_user = User.login(manager, username, password)
    if not current_user:
        return Response(b"User is not authenticated", 403, 'text/plain')
    
    def f(x):
        x.created_at = str(x.created_at)
        return x.to_dict()
    user_inbox = list(map(f,filter(lambda msg: msg.reciever_id == current_user._id, manager.read_all(Message))))

    return Response(json.dumps({'messages':user_inbox}).encode(), 200)