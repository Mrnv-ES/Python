import re
import csv


def get_value(my_str):
    reg_exp = r'^.*:\s*'
    return re.split(reg_exp, my_str)


def get_data(file_lst):
    main_data = [['Изготовитель ОС', 'Название ОС', 'Код продукта', 'Тип системы']]

    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []

    for file in file_lst:
        try:
            with open(file, 'r', encoding='windows-1251') as opened_file:
                for line in opened_file:
                    if 'Изготовитель ОС' in line:
                        value_lst = get_value(line)
                        os_prod_list.append(value_lst[1].rstrip())
                    elif 'Название ОС' in line:
                        value_lst = get_value(line)
                        os_name_list.append(value_lst[1].rstrip())
                    elif 'Код продукта' in line:
                        value_lst = get_value(line)
                        os_code_list.append(value_lst[1].rstrip())
                    elif 'Тип системы' in line:
                        value_lst = get_value(line)
                        os_type_list.append(value_lst[1].rstrip())
        except FileNotFoundError:
            print(f'файла {file} не существует')

    max_len = max(len(os_code_list), len(os_name_list), len(os_prod_list), len(os_type_list))

    for count in range(max_len):
        try:
            new_main_data = []
            new_main_data.append(os_prod_list[count])
            new_main_data.append(os_name_list[count])
            new_main_data.append(os_code_list[count])
            new_main_data.append(os_type_list[count])
        except IndexError:
            print('Необходимы значения каждого из параметров')

        main_data.append(new_main_data)

    return main_data


def write_to_csv(file):
    files = ['info_1.txt', 'info_2.txt', 'info_3.txt']

    data = get_data(files)

    with open(file, 'w', encoding='utf-8') as written_file:
        csv_writer = csv.writer(written_file, quoting=csv.QUOTE_NONNUMERIC)
        for row in data:
            csv_writer.writerow(row)


write_to_csv('report_file.csv')
