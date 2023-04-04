import socket
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random
import multiprocessing as mp

ids = ["B2","B5","B10","G2","G5","G10"]


def OCChost(vals):
    class handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            with open('ProjectOCC.html') as message:
                message = message.read()
                for id in ids:
                    message= message.replace("||"+id+"||",str(vals[id]))
                self.wfile.write(bytes(message, "utf8"))
                print(vals)

    print("Open Webpage")
    with HTTPServer(('', 8000), handler) as server:
        server.serve_forever()

def OCCserver(vals):
    vals = {"B2":0,"B5":0,"B10":0,"G2":0,"G5":0,"G10":0}
    s = socket.socket()
    host = "127.0.0.1"
    port = 5409
    s.bind((host, port))
    s.listen(100)

    print("Open Server")
    while True:
        conn, addr = s.accept()  
        print('Got connection from', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = data.decode("utf-8")
            print(data)
            val = data.split(",")
            print(val)

            for id in ids:
                vals[id] = val[ids.index(id)]

            print(vals)

if __name__ == '__main__':
    manager = mp.Manager()
    vals = manager.dict()
    vals = {"B2":0,"B5":0,"B10":0,"G2":0,"G5":0,"G10":0}

    p2 = mp.Process(target=OCCserver, args=(vals,))
    p1 = mp.Process(target=OCChost, args=(vals,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
    #a()