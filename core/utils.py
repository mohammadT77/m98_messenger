from dataclasses import dataclass


@dataclass
class Response:
    content: bytes  # content
    status_code: int = 200
    content_type: str = "application/json"

@dataclass
class Request:
    method: str # GET, POST, DELETE, PUT, PATCH, HEAD, OPTION
    path: str  # /, /message, /user, /message/sent, /login
    urlparams: dict  # {'name':'Akbar'}
    body: bytes  
    headers: any  # Content-Type, Content-Length, ...