import yaml

data = {
    1: ['hi', 4243, True],
    2: 7777777,
    3: {1: '\u2605', 2: '\u049c', 3: '\u2118'}
}


def write_file():
    with open('my_yaml.yaml', 'w', encoding='utf-8') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False, allow_unicode=True)


def read_file():
    try:
        with open('my_yaml.yaml', 'r', encoding='utf-8') as file_to_read:
            content = yaml.load(file_to_read)
            return content
    except FileNotFoundError:
        print('файл не найден')


write_file()
print(read_file())
