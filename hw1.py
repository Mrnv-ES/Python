# Task 1
my_list = ['разработка', 'сокет', 'декоратор']
for el in my_list:
    print(f'Тип данных: {type(el)}, содержание переменной: "{el}"')

unicode_list = [
    '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
    '\u0441\u043e\u043a\u0435\u0442',
    '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440',
    ]
for el in unicode_list:
    print(f'Тип данных: {type(el)}, содержание переменной: "{el}"')


# Task 2
bytes_list = [b'class', b'function', b'method']
for el in bytes_list:
    print(f'Тип: {type(el)}, содержание: {el}, длина: {len(el)}')


# Task 3
bytes_check_list = [b'attribute', b'класс', b'функция', b'type']
for el in bytes_check_list:
    print(el)

# File "C:/Users/Катя/ThirdQ/hw1.py", line 22
#     bytes_check_list = [b'attribute', b'класс', b'функция', b'type']
#                                       ^
# SyntaxError: bytes can only contain ASCII literal characters.
# Слова 'класс' и 'функция' невозможно записать в байтовом типе,
# т.к. русские буквы не относятся к ASCII


# Task 4
my_lst = ['разработка', 'администрирование', 'protocol', 'standard']
for el in my_lst:
    in_bytes = el.encode('utf-8')
    print(f'Байтовое представление: {in_bytes}')
    in_str = in_bytes.decode('utf-8')
    print(f'Строковое: {in_str}')


# Task 5
import subprocess

info = [['ping', 'yandex.ru'], ['ping', 'youtube.com']]
for info_el in info:
    do_ping = subprocess.Popen(info_el, stdout=subprocess.PIPE)
    for line in do_ping.stdout:
        print(line)

    # for line in do_ping.stdout:
    #     print(line.decode('utf-8'))
    #
    ## Traceback (most recent call last):
    ##   File "C:/Users/Катя/ThirdQ/hw1.py", line 51, in <module>
    ##     print(line.decode('utf-8'))
    ## UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8e in position 0: invalid start byte

    for line in do_ping.stdout:
        line = line.decode('cp866').encode('utf-8')
        print(line.decode('utf-8'))
    ## Обмен пакетами с yandex.ru [77.88.55.55] с 32 байтами данных:
    ## Ответ от 77.88.55.55: число байт=32 время=4мс TTL=249
    ## Ответ от 77.88.55.55: число байт=32 время=5мс TTL=249
    ## Ответ от 77.88.55.55: число байт=32 время=4мс TTL=249
    ## Ответ от 77.88.55.55: число байт=32 время=4мс TTL=249
    ## Статистика Ping для 77.88.55.55:
    ##     Пакетов: отправлено = 4, получено = 4, потеряно = 0
    ##     (0% потерь)
    ## Приблизительное время приема-передачи в мс:
    ##     Минимальное = 4мсек, Максимальное = 5 мсек, Среднее = 4 мсек
    ##
    ##
    ## Обмен пакетами с youtube.com [173.194.220.136] с 32 байтами данных:
    ## Ответ от 173.194.220.136: число байт=32 время=18мс TTL=59
    ## Ответ от 173.194.220.136: число байт=32 время=18мс TTL=59
    ## Ответ от 173.194.220.136: число байт=32 время=18мс TTL=59
    ## Ответ от 173.194.220.136: число байт=32 время=27мс TTL=59
    ## Статистика Ping для 173.194.220.136:
    ##     Пакетов: отправлено = 4, получено = 4, потеряно = 0
    ##     (0% потерь)
    ## Приблизительное время приема-передачи в мс:
    ##     Минимальное = 18мсек, Максимальное = 27 мсек, Среднее = 20 мсек


# Task 6
import locale
my_coding = locale.getpreferredencoding()
print(my_coding)


lines = ["сетевое программирование", "сокет", "декоратор"]

with open('test_file.txt', 'w', encoding='utf-8') as t_f:
    for line in lines:
        t_f.write(line + '\n')

t_f.close()
print(t_f)
# <_io.TextIOWrapper name='test_file.txt' mode='w' encoding='cp1251'>

with open('test_file.txt', 'r', encoding='utf-8') as t_f:
    for line in t_f:
        print(line)
