import argparse
import select
import socket
import sys
import time
from hw8.utilities import load_configs, get_msg, send_msg
import logging
from hw8.dec import log
import hw8.server_log_config

CONFIGS = dict()
SERVER_LOGGER = logging.getLogger('server')


@log
def manage_msg(msg, msg_list, client, CONFIGS):
    global SERVER_LOGGER
    SERVER_LOGGER.debug(f'Обрабатывается сообщение клиента : {msg}')
    if CONFIGS.get('ACTION') in msg \
            and msg[CONFIGS.get('ACTION')] == CONFIGS.get('PRESENCE') \
            and CONFIGS.get('TIME') in msg \
            and CONFIGS.get('USER') in msg \
            and msg[CONFIGS.get('USER')][CONFIGS.get('ACCOUNT_NAME')] == 'Guest':
        msg_list.append({CONFIGS.get('RESPONSE'): 200})
        SERVER_LOGGER.info('Ответ от сервера успешно получен')
    SERVER_LOGGER.error('Некорректное сообщение от клиента')
    msg_list.append({
        CONFIGS.get('RESPONSE'): 400,
        CONFIGS.get('ERROR'): 'Bad Request'
    })


def arg_parsing(CONFIGS):
    global SERVER_LOGGER
    parsing = argparse.ArgumentParser()
    parsing.add_argument('-p', default=CONFIGS['DEFAULT_PORT'], type=int, nargs='?')
    parsing.add_argument('-a', default='', nargs='?')
    namespace = parsing.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Значение порта {listen_port} некорректно.'
                               'Порт должен быть в пределах от 1024 до 65535.')
        sys.exit(1)

    return listen_address, listen_port


def main():
    global CONFIGS, SERVER_LOGGER
    CONFIGS = load_configs()
    listen_addr, listen_port = arg_parsing(CONFIGS)
    SERVER_LOGGER.info(f'Сервер запущен на порту №{listen_port}, адрес: {listen_addr}.')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((listen_addr, listen_port))
    sock.settimeout(0.9)

    clients_lst = []
    msg_lst = []

    sock.listen(CONFIGS.get('MAX_CONNECTIONS'))

    while True:
        try:
            client, client_addr = sock.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Соедение с пользователем по адресу: {client_addr}')
            clients_lst.append(client)

        recv_data_list = []
        send_data_list = []
        error_list = []
        try:
            if clients_lst:
                recv_data_list, send_data_list, error_list = select.select(clients_lst, clients_lst, [], 0)
        except OSError:
            pass

        if recv_data_list:
            for client_with_msg in recv_data_list:
                try:
                    manage_msg(get_msg(client_with_msg, CONFIGS), msg_lst, client_with_msg,
                                   CONFIGS)
                except:
                    SERVER_LOGGER.info(f'Пользователь {client_with_msg.getpeername()} отключился от сервера.')
                    clients_lst.remove(client_with_msg)

        if msg_lst and send_data_list:
            message = {
                CONFIGS['TIME']: time.time(),
                CONFIGS['SENDER']: msg_lst[0][0],
                CONFIGS['MESSAGE_TEXT']: msg_lst[0][1],
                CONFIGS['ACTION']: CONFIGS['MESSAGE'],
            }
            del msg_lst[0]
            for waiting_client in send_data_list:
                try:
                    send_msg(waiting_client, message, CONFIGS)
                except:
                    SERVER_LOGGER.info(f'Пользователь {waiting_client.getpeername()} отключился от сервера.')
                    clients_lst.remove(waiting_client)


if __name__ == '__main__':
    main()
