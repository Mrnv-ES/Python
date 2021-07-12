from socket import *
import select


def read_requests(r_client, w_client, clients_list):
    for r_sock in r_client:
        try:
            msg = r_sock.recv(1024)
            for w_sock in w_client:
                try:
                    w_sock.send(msg)
                except Exception as err:
                    clients_list.remove(w_sock)
        except Exception as err:
            # print(err)
            pass


sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('127.0.0.1', 7777))
sock.listen(7)
sock.settimeout(0.2)

all_clients = []

while True:
    try:
        client, addr = sock.accept()
        all_clients.append(client)
    except OSError as e:
        print(e)

    r = []
    w = []

    try:
        r, w, e = select.select(all_clients, all_clients, [], 0)
    except Exception as err:
        # print(err)
        pass

    read_requests(r, w, all_clients)
