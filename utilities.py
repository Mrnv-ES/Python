import sys
import json
import os


def load_configs(is_server=True):
    config_keys = [
        'DEFAULT_PORT',
        'MAX_CONNECTIONS',
        'MAX_PACKAGE_LENGTH',
        'ENCODING',
        'ACTION',
        'TIME',
        'USER',
        'ACCOUNT_NAME',
        'PRESENCE',
        'RESPONSE',
        'ERROR'
    ]
    if not is_server:
        config_keys.append('DEFAULT_IP_ADDRESS')
    if not os.path.exists('config.json'):
        print('Файл не найден')
        sys.exit(1)
    with open('config.json') as configs:
        CONFIGS = json.load(configs)
    loaded_config_keys = list(CONFIGS.keys())
    for key in config_keys:
        if key not in loaded_config_keys:
            print(f'В файле не хватает ключа: {key}')
            sys.exit(1)
    return CONFIGS


def send_msg(opened_sock, msg, CONFIGS):
    json_msg = json.dumps(msg)
    response = json_msg.encode(CONFIGS.get('ENCODING'))
    opened_sock.send(response)


def get_msg(opened_sock, CONFIGS):
    response = opened_sock.recv(CONFIGS.get('MAX_PACKAGE_LENGTH'))
    if isinstance(response, bytes):
        json_response = response.decode(CONFIGS.get('ENCODING'))
        response_dict = json.loads(json_response)
        if isinstance(response_dict, dict):
            return response_dict
        raise ValueError
    raise ValueError
