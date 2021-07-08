import socket
import json
import sys
from hw5.utilities import load_configs, get_msg, send_msg
import logging
from hw6.dec import log
import hw6.server_log_config

CONFIGS = dict()
SERVER_LOGGER = logging.getLogger('server')


@log
def manage_msg(msg, CONFIGS):
    if CONFIGS.get('ACTION') in msg \
            and msg[CONFIGS.get('ACTION')] == CONFIGS.get('PRESENCE') \
            and CONFIGS.get('TIME') in msg \
            and CONFIGS.get('USER') in msg \
            and msg[CONFIGS.get('USER')][CONFIGS.get('ACCOUNT_NAME')] == 'Guest':
        SERVER_LOGGER.info('Ответ от сервера успешно получен')
        return {CONFIGS.get('RESPONSE'): 200}
    SERVER_LOGGER.error('Некорректное сообщение от клиента')
    return {
        CONFIGS.get('RESPONSE'): 400,
        CONFIGS.get('ERROR'): 'Bad Request'
    }


def main():
    global CONFIGS, SERVER_LOGGER
    CONFIGS = load_configs()
    listen_port = CONFIGS.get('DEFAULT_PORT')
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            SERVER_LOGGER.info('Значение порта указано корректно')
        if not 1024 <= listen_port <= 65535:
            raise ValueError
    except IndexError:
        SERVER_LOGGER.critical('После -p нужно указать номер порта')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.critical(f'Некорректный порт {listen_port}. Номер порта должен быть от 1024 до 65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_addr = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_addr = ''
    except IndexError:
        SERVER_LOGGER.info('После -a нужно указать адрес')
        sys.exit(1)

    SERVER_LOGGER.info(f'Сервер запущен на порту {listen_port} по адресу {listen_addr}')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((listen_addr, listen_port))
    sock.listen(CONFIGS.get('MAX_CONNECTIONS'))

    while True:
        client, client_addr = sock.accept()
        try:
            msg = get_msg(client, CONFIGS)
            response = manage_msg(msg, CONFIGS)
            send_msg(client, response, CONFIGS)
            client.close()
        except (ValueError, json.JSONDecodeError):
            SERVER_LOGGER.critical('Сообщение от клиента некорректно')
            client.close()


if __name__ == '__main__':
    main()
