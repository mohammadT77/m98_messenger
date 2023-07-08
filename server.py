from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from core.utils import *
from core.views import *


routes = {
    ('GET', '/user'): get_user,
    ('PATCH', '/user'): change_name,
    ('POST', '/user'): register_user,

    ('POST', '/message'): create_message,
    ('GET', '/message/inbox'): inbox,
    ('GET', '/message/sent'): sentbox,
}


class MessengerRequestHandler(SimpleHTTPRequestHandler):

    def handle_request(self, method):
        # Read request
        path, _, params = self.path.partition('?')  #  self.path = "/message/create?x=10&y=20"
        if self.command == 'POST':
            content_len = int(self.headers.get('Content-Length') or 0)
            request_body = self.rfile.read(content_len)
        else:
            request_body = b''

        req = Request(
            method=self.command,
            path=path, 
            urlparams=parse_qs(params), # ?x=1&y=2 -> {'x':['1'], 'y':['2']}
            body=request_body,
            headers=self.headers
        )        
        
        # Route request
        view_func = routes.get((method, path), None)
        if not view_func:
            resp = Response(b"Not found", 404, content_type='text/plain')    
        else:
            resp = view_func(req)


        # prepare & send Response
        self.send_response(resp.status_code)
        self.send_header("Content-Type", resp.content_type)
        self.end_headers()
        self.wfile.write(resp.content)

    
    def do_GET(self) -> None:
        self.handle_request('GET')

    def do_POST(self) -> None:
        self.handle_request('POST')

    def do_PATCH(self) -> None:
        self.handle_request('PATCH')
    
print("Please make sure you are connected to database and tables are created there.")

host_port = ("0.0.0.0", 8000)
server = HTTPServer(host_port, MessengerRequestHandler)
print("Starting server on:", host_port)
server.serve_forever()  # while true:


