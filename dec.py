import inspect
import logging
import sys

if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


def log(func):
    def save_log(*args, **kwargs):
        func_res = func(*args, **kwargs)
        LOGGER.info(f'Функция {func.__name__} была вызвана из функции {inspect.stack()[1][3]}')
        return func_res
    return save_log


class Log:
    def __call__(self, func):
        def save_log(*args, **kwargs):
            func_res = func(*args, **kwargs)
            LOGGER.info(f'Функция {func.__name__} была вызвана из функции {inspect.stack()[1][3]}')
            return func_res
        return save_log
