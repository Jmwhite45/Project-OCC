init = {
    "Goal": 100,
    "Dev": .1
}

import socket
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random
from multiprocessing import Process, Manager

ids = ["B2","B5","B10","G2","G5","G10"]
settings = {
    "Goal": init["Goal"],
    "Dev": init["Dev"],
    "Threshhold": .5
}

def stage(currValue, total):
    if(total<settings["Goal"]*settings["Threshhold"]):
        return "#00ff00"
    
    if(currValue<total/6*(1-2*settings["Dev"])): #Very Low
        return "#0000ff"
    if(currValue<total/6*(1-settings["Dev"])): # Low
        return "#00ffff"
    if(currValue<total/6*(1+settings["Dev"])): # Normal
        return "#00ff00"
    if(currValue<total/6*(1-2*settings["Dev"])): #high
        return "#ffff00"
    else:
        return "#c40606" # Very HJigh
settings["stage"] = stage



def OCChost(vals):
    print(settings)
    class handler(BaseHTTPRequestHandler):
        def do_GET(self):
            print(vals)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            with open('ProjectOCC.html') as message:
                message = message.read()
                sumVals = 0
                for id in ids:
                    sumVals+=int(vals[id])

                for id in ids:
                    message= message.replace("||"+id+"||",str(vals[id]))
                    message = message.replace("||"+id+"-color||", settings["stage"](vals[id],sumVals))
                message = message.replace("||Goal||",str(sumVals/settings["Goal"]*100))
                
                self.wfile.write(bytes(message, "utf8"))
                print(vals)

    print("Open Webpage")
    with HTTPServer(('', 8000), handler) as server:
        server.serve_forever()

def OCCserver(vals):
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
                vals[id] = int(val[ids.index(id)])

            print(vals)

if __name__ == '__main__':
    manager = Manager()
    vals = manager.dict()

    for id in ids:
        vals[id] = 0

    p2 = Process(target=OCCserver, args=(vals,))
    p2.start()

    p1 = Process(target=OCChost, args=(vals,))
    p1.start()

    p2.join()
    p1.join()