import argparse
import socket
import sys
import threading
import time
import json
from hw5.utilities import load_configs, get_msg, send_msg
import logging
from hw8.dec import Log
import hw8.client_log_config
from hw8.err import RequiredFieldMissingError, ServerError, IncorrectDataReceivedError

CONFIGS = dict()
CLIENT_LOGGER = logging.getLogger('client')


def help_text():
    print('Поддерживаемые команды:')
    print('msg - отправить сообщение')
    print('help - вывести подсказки по командам')
    print('exit - выход')


@Log()
def make_exit_msg(account_name):
    return {
        CONFIGS['TIME']: time.time(),
        CONFIGS['ACCOUNT_NAME']: account_name,
        CONFIGS['ACTION']: CONFIGS['EXIT'],
    }


@Log()
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


def get_user_msg(sock, CONFIGS, account_name='Guest'):
    msg = input('Введите сообщение для отправки или \'q\' для завершения работы: ')
    if msg == 'q':
        sock.close()
        CLIENT_LOGGER.info('Пользователь завершил работу.')
        sys.exit(0)
    msg_dict = {
        CONFIGS['TIME']: time.time(),
        CONFIGS['ACCOUNT_NAME']: account_name,
        CONFIGS['MESSAGE_TEXT']: msg,
        CONFIGS['ACTION']: CONFIGS['MESSAGE']
    }
    CLIENT_LOGGER.debug(f'Был создан словарь сообщения: {msg_dict}')
    return msg_dict


def create_msg(sock, account_name='Guest'):
    to_user = input('Кому отправить сообщение: ')
    msg = input('Текст сообщения: ')
    msg_dict = {
        CONFIGS['SENDER']: account_name,
        CONFIGS['DESTINATION']: to_user,
        CONFIGS['TIME']: time.time(),
        CONFIGS['MESSAGE_TEXT']: msg,
        CONFIGS['ACTION']: CONFIGS['MESSAGE']
    }
    CLIENT_LOGGER.debug(f'Был создан словарь сообщения: {msg_dict}')
    try:
        CLIENT_LOGGER(sock, msg_dict, CONFIGS)
        CLIENT_LOGGER.info(f'Было отправлено сообщение для {to_user}')
    except:
        CLIENT_LOGGER.critical('Была потеряна связь с сервером.')
        sys.exit(1)


def manage_server_msg(msg, CONFIG):
    if CONFIG['ACTION'] in msg and msg[CONFIG['ACTION']] == CONFIG['MESSAGE'] and \
            CONFIG['SENDER'] in msg and CONFIG['MESSAGE_TEXT'] in msg:
        print(f'Было получено сообщение от '
              f'{msg[CONFIG["SENDER"]]}:\n{msg[CONFIG["MESSAGE_TEXT"]]}')
        CLIENT_LOGGER.info(f'Было получено сообщение от '
                           f'{msg[CONFIG["SENDER"]]}:\n{msg[CONFIG["MESSAGE_TEXT"]]}')
    else:
        CLIENT_LOGGER.error(f'Было получено некорректное сообщение с сервера: {msg}')


@Log()
def arg_parsing(CONFIGS):
    global CLIENT_LOGGER
    parsing = argparse.ArgumentParser()
    parsing.add_argument('addr', default=CONFIGS['DEFAULT_IP_ADDRESS'], nargs='?')
    parsing.add_argument('port', default=CONFIGS['DEFAULT_PORT'], type=int, nargs='?')
    parsing.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parsing.parse_args(sys.argv[1:])

    server_addr = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(f'Значение порта {server_port} некорректно.'
                               'Порт должен быть в пределах от 1024 до 65535.')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Недопустимый режим работы {client_mode}, допустимые режимы: listen , send')
        sys.exit(1)

    return server_addr, server_port, client_mode

@Log()
def manage_response(msg, CONFIGS):
    CLIENT_LOGGER.info('Обработка сообщения от сервера')
    if CONFIGS.get('RESPONSE') in msg:
        if msg[CONFIGS.get('RESPONSE')] == 200:
            CLIENT_LOGGER.info('Обработка сообщения от сервера успешно завершена')
            return '200 : Ok'
        CLIENT_LOGGER.error('Обработка сообщения от сервера была завершена с ошибкой')
        return f'400 : {msg[CONFIGS.get("ERROR")]}'
    raise ValueError


@Log()
def msg_from_server(sock, username):
    while True:
        try:
            msg = get_msg(sock, CONFIGS)
            if CONFIGS['ACTION'] in msg and msg[CONFIGS['ACTION']] == CONFIGS['MESSAGE'] and \
                    CONFIGS['SENDER'] in msg and CONFIGS['DESTINATION'] in msg \
                    and CONFIGS['MESSAGE_TEXT'] in msg and msg[CONFIGS['DESTINATION']] == username:
                print(f'\nБыло получено ообщение от {msg[CONFIGS["SENDER"]]}:'
                      f'\n{msg[CONFIGS["MESSAGE_TEXT"]]}')
                CLIENT_LOGGER.info(f'Было получено ообщение от {msg[CONFIGS["SENDER"]]}:'
                            f'\n{msg[CONFIGS["MESSAGE_TEXT"]]}')
            else:
                CLIENT_LOGGER.error(f'Было получено некорректное сообщение от сервера: {msg}')
        except IncorrectDataReceivedError:
            CLIENT_LOGGER.error(f'Не удалось декодировать полученное сообщение.')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            CLIENT_LOGGER.critical(f'Была потеряна связь с сервером.')
            break


def user_interactive(sock, username):
    print(help_text())
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_msg(sock, username)
        elif command == 'help':
            print(help_text())
        elif command == 'exit':
            send_msg(sock, make_exit_msg(username), CONFIGS)
            print('Завершение соединения.')
            CLIENT_LOGGER.info('Пользователь завершил работу.')
            time.sleep(0.5)
            break
        else:
            print('Попробойте снова. help - вывести допустимые команды.')


def main():
    global CONFIGS, CLIENT_LOGGER
    CONFIGS = load_configs(is_server=False)
    server_addr, server_port, client_mode = arg_parsing(CONFIGS)
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_addr, server_port))
        send_msg(transport, make_presence_msg(CONFIGS), CONFIGS)
        answer = manage_response(get_msg(transport, CONFIGS), CONFIGS)
        CLIENT_LOGGER.info(f'Было установлено соединение с сервером, ответ: {answer}')
        print(f'Было установлено соединение с сервером.')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Декодирование полученной Json строки провалилось.')
        sys.exit(1)
    except ServerError as error:
        CLIENT_LOGGER.error(f'Ошибка сервера при попытке установить соединение: {error.text}')
        sys.exit(1)
    except RequiredFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует  поле {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(
            f'Подключение к серверу {server_addr}:{server_port} провалилось, '
            f'компьютер пользователя отверг запрос на подключение.')
        sys.exit(1)
    else:
        client_name = ''
        receiver = threading.Thread(target=msg_from_server, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(target=user_interactive, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()
        CLIENT_LOGGER.debug('Были запущены процессы')


if __name__ == '__main__':
    main()
