from socket import *

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('127.0.0.1', 7777))

while True:
    msg = input('Type the message: ').encode('utf-8')
    sock.send(msg)
