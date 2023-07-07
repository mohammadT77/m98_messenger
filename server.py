from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from core.utils import *
from core.views import *


routes = {
    ('POST', '/msg/create'): create_message,
    ('GET', '/inbox'): inbox,
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



server = HTTPServer(("0.0.0.0", 8000), MessengerRequestHandler)
server.serve_forever()  # while true:
print("AKBAR BABAII")


