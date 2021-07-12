from socket import *

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('127.0.0.1', 7777))


while True:
    response = sock.recv(1024)
    if response:
        data = response.decode('utf-8')
        print(data)
    else:
        continue
