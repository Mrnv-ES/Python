import logging
import sys
import os
import logging.handlers
from hw5.utilities import load_configs

sys.path.append('../')

CONFIGS = load_configs()

SERVER_FORMATTER = logging.Formatter('%(levelname)s %(filename)s %(asctime)s %(message)s')

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')

STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf-8', interval=1, when='D')
LOG_FILE.setFormatter(SERVER_FORMATTER)

LOGGER = logging.getLogger('server')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(CONFIGS.get('LOGGING_LEVEL', logging.DEBUG))

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.info('Информационное сообщение')
    LOGGER.debug('Отладочная информация')
