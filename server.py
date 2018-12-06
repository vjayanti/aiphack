from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import json
import os
from subprocess import call
import base64

class ManagerServer(ThreadingMixIn, HTTPServer):
    def __init__(self, address, handler):
        HTTPServer.__init__(self, address, handler)


class ManagerRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        print(self.path)
        try:
            if self.path == "/decrypt":
                username = self.headers.getheader('username')
                password = self.headers.getheader('password')
                content_len = int(self.headers.getheader('content-length', 0))
                file = self.rfile.read(content_len)
                with open('file.in.docx', 'w') as tmp:
                     tmp.write(file)
                self.send_response(200)
                self.end_headers()
                call(["./mip_driver.decrypt.exe", "--username", username, "--password", password, "--file", "file.in.docx", "--fileOut", "file.tmp.docx", "--decrypt"])
                with open('file.out.tmp') as tmp:
                     self.wfile.write(base64.b64decode(tmp.read()))
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
        elif self.path == "/checkIsProtected":
            username = self.headers.getheader('username')
            password = self.headers.getheader('password')
            content_len = int(self.headers.getheader('content-length', 0))
            file = self.rfile.read(content_len)
            with open('file.in.docx', 'w') as tmp:
                 tmp.write(file)
            exitCode = call(["./mip_driver.exe", "--username", username, "--password", password, "--file", "file.in.docx", "--checkIsProtected"])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(exitCode)
        elif self.path == "/checkIsLabeled":
            username = self.headers.getheader('username')
            password = self.headers.getheader('password')
            content_len = int(self.headers.getheader('content-length', 0))
            file = self.rfile.read(content_len)
            with open('file.in.docx', 'w') as tmp:
                 tmp.write(file)
            exitCode = call(["./mip_driver.exe", "--username", username, "--password", password, "--file", "file.in.docx", "--checkIsLabeled"])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(exitCode)
        elif self.path == "/checkHasWatermark":
            username = self.headers.getheader('username')
            password = self.headers.getheader('password')
            content_len = int(self.headers.getheader('content-length', 0))
            file = self.rfile.read(content_len)
            with open('file.in.docx', 'w') as tmp:
                 tmp.write(file)
            exitCode = call(["./mip_driver.exe", "--username", username, "--password", password, "--file", "file.in.docx", "--checkHasWatermark"])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(exitCode)
   
PORT = 10000

Handler = ManagerRequestHandler

httpd = ManagerServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
