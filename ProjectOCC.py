from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random

html = open('ProjectOCC.html')

ids = ["B2","B5","B10","G2","G5","G10"]
vals = {"B2":0,"B5":0,"B10":0,"G2":0,"G5":0,"G10":0}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = open('ProjectOCC.html').read()
        for id in ids:
            message= message.replace("||"+id+"||",str(vals[id]))
        self.wfile.write(bytes(message, "utf8"))

        vals[random.choice(ids)] +=1

with HTTPServer(('', 8000), handler) as server:
    server.serve_forever()