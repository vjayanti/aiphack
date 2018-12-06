from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import json
import os

class ManagerServer(ThreadingMixIn, HTTPServer):
    def __init__(self, address, handler):
        HTTPServer.__init__(self, address, handler)


class ManagerRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        print(self.path)
        try:
            if self.path == "/cover_shifts":
                start = self.headers.getheader('start')
                end = self.headers.getheader('end')
                group_id = self.headers.getheader('group')
                print(message)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(message)
            elif self.path == "/swap_shifts":
                old_time = self.headers.getheader('old_time')
                new_time = self.headers.getheader('new_time')
                from_person = self.headers.getheader('from_person')
                to_person = self.headers.getheader('to_person')
                print(old_time, new_time, from_person, to_person)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(message)
            else:
                self.send_response(404)
        except Exception as e:
            print(e)
            self.send_response(400)
            self.end_headers()
            self.wfile.write(str(e))

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write('hello world')

PORT = 10000

Handler = ManagerRequestHandler

httpd = ManagerServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
