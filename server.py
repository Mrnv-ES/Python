import socket
import json
import sys
from hw3.utilities import load_configs, get_msg, send_msg

CONFIGS = dict()


def manage_msg(msg):
    if CONFIGS.get('ACTION') in msg \
            and msg[CONFIGS.get('ACTION')] == CONFIGS.get('PRESENCE') \
            and CONFIGS.get('TIME') in msg \
            and CONFIGS.get('USER') in msg \
            and msg[CONFIGS.get('USER')][CONFIGS.get('ACCOUNT_NAME')] == 'Guest':
        return {CONFIGS.get('RESPONSE'): 200}
    return {
        CONFIGS.get('RESPONSE'): 400,
        CONFIGS.get('ERROR'): 'Bad Request'
    }


def main():
    global CONFIGS
    CONFIGS = load_configs()
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = CONFIGS.get('DEFAULT_PORT')
        if not 1024 <= listen_port <= 65535:
            raise ValueError
    except IndexError:
        print('После -p нужно указать номер порта')
        sys.exit(1)
    except ValueError:
        print('Номер порта должен быть от 1024 до 65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_addr = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_addr = ''
    except IndexError:
        print('После -a нужно указать адрес')
        sys.exit(1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((listen_addr, listen_port))
    sock.listen(CONFIGS.get('MAX_CONNECTIONS'))

    while True:
        client, client_addr = sock.accept()
        try:
            msg = get_msg(client, CONFIGS)
            response = manage_msg(msg)
            send_msg(client, response, CONFIGS)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Сообщение от клиента некорректно')
            client.close()


if __name__ == '__main__':
    main()
