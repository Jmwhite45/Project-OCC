import socket   
import sys

if len(sys.argv)<2:
    exit()

s = socket.socket()         
host = "127.0.0.1"         
port = 5409            

val =""
for arg in sys.argv[1:]:
    val += arg+","
val = val[:-1]
s.connect((host, port))
s.send(bytes(val, 'utf-8'))
s.close() 