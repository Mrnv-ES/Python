import socket
import sys
import time
import json
from hw3.utilities import load_configs, get_msg, send_msg
import logging

CONFIGS = dict()
CLIENT_LOGGER = logging.getLogger('client')


def make_presence_msg(account_name, CONFIGS):
    msg = {
        CONFIGS.get('ACTION'): CONFIGS.get('PRESENCE'),
        CONFIGS.get('TIME'): time.time(),
        CONFIGS.get('USER'): {
            CONFIGS.get('ACCOUNT_NAME'): account_name
        }
    }
    CLIENT_LOGGER.info('Сообщение для отправки на сервер')
    return msg


def manage_response(msg, CONFIGS):
    CLIENT_LOGGER.info('Обработка сообщения от сервера')
    if CONFIGS.get('RESPONSE') in msg:
        if msg[CONFIGS.get('RESPONSE')] == 200:
            CLIENT_LOGGER.info('Обработка сообщения от сервера успешно завершена')
            return '200 : Ok'
        CLIENT_LOGGER.error('Обработка сообщения от сервера была завершена с ошибкой')
        return f'400 : {msg[CONFIGS.get("ERROR")]}'
    raise ValueError


def main():
    global CONFIGS, CLIENT_LOGGER
    CONFIGS = load_configs(is_server=False)
    try:
        server_addr = sys.argv[1]
        server_port = int(sys.argv[2])
        CLIENT_LOGGER.info('Значения порта и адреса корректны')
        if not 1024 <= server_port <= 65535:
            raise ValueError
    except IndexError:
        server_addr = CONFIGS.get('DEFAULT_IP_ADDRESS')
        server_port = CONFIGS.get('DEFAULT_PORT')
        CLIENT_LOGGER.warning('Порт и адрес были заданы неверно, поэтому были установлены дефолтные значения')
    except ValueError:
        CLIENT_LOGGER.critical('Номер порта должен быть от 1024 до 65535')
        sys.exit(1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_addr, server_port))
    presence_msg = make_presence_msg('Guest', CONFIGS)
    CLIENT_LOGGER.info('Отправка сообщения серверу')
    send_msg(sock, presence_msg, CONFIGS)
    try:
        response = get_msg(sock, CONFIGS)
        managed_response = manage_response(response, CONFIGS)
        CLIENT_LOGGER.debug(f'Ответ от сервера: {response}')
        CLIENT_LOGGER.info(f'Обработанный ответ от сервера: {managed_response}')
    except(ValueError, json.JSONDecodeError):
        CLIENT_LOGGER.critical('Ошибка при декодировании сообщения')


if __name__ == '__main__':
    main()
