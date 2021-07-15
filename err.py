class IncorrectDataReceivedError(Exception):
    def __str__(self):
        return 'Некорректное сообщение от удалённого компьютера.'


class ServerError(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class NonDictInputError(Exception):
    def __str__(self):
        return 'Аргумент функции должен быть словарём.'


class RequiredFieldMissingError(Exception):
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'Отсутствует поле {self.missing_field}.'