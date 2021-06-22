import socket
import sys
import time
import json
from hw3.utilities import load_configs, get_msg, send_msg

CONFIGS = dict()


def make_presence_msg(account_name):
    msg = {
        CONFIGS.get('ACTION'): CONFIGS.get('PRESENCE'),
        CONFIGS.get('TIME'): time.time(),
        CONFIGS.get('USER'): {
            CONFIGS.get('ACCOUNT_NAME'): account_name
        }
    }
    return msg


def manage_response(msg):
    if CONFIGS.get('RESPONSE') in msg:
        if msg[CONFIGS.get('RESPONSE')] == 200:
            return '200 : Ok'
        return f'400 : {msg[CONFIGS.get("ERROR")]}'
    raise ValueError


def main():
    global CONFIGS
    CONFIGS = load_configs(is_server=False)
    try:
        server_addr = sys.argv[1]
        server_port = int(sys.argv[2])
        if not 1024 <= server_port <= 65535:
            raise ValueError
    except IndexError:
        server_addr = CONFIGS.get('DEFAULT_IP_ADDRESS')
        server_port = CONFIGS.get('DEFAULT_PORT')
    except ValueError:
        print('Номер порта должен быть от 1024 до 65535')
        sys.exit(1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_addr, server_port))
    presence_msg = make_presence_msg('Guest')
    send_msg(sock, presence_msg, CONFIGS)
    try:
        response = get_msg(sock, CONFIGS)
        managed_response = manage_response(response)
        print(f'Ответ сервера: {response}')
        print(managed_response)
    except(ValueError, json.JSONDecodeError):
        print('Ошибка при декодировании сообщения')


if __name__ == '__main__':
    main()
