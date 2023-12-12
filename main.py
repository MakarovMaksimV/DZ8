from os.path import exists
from csv import DictReader, DictWriter

class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt

class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt

class LastNameError(Exception):
    def __init__(self, txt):
        self.txt = txt

class RowError(Exception):
    def __init__(self, txt):
        self.txt = txt

def get_info():
    is_valid_first_name = False
    while not is_valid_first_name:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise NameError("Не валидное имя")
            else:
                is_valid_first_name = True
        except NameError as err:
            print(err)
            continue
    is_valid_last_name = False
    while not is_valid_last_name:
        try:
            last_name = input("Введите фамилию: ")
            if len(last_name) < 2:
                raise LastNameError("Не валидная фамилия")
            else:
                is_valid_last_name = True
        except LastNameError as err:
            print(err)
            continue
    is_valid_phone = False
    while not is_valid_phone:
        try:
            phone_number = int(input("Введите номер: "))
            if len(str(phone_number)) != 11:
                raise LenNumberError("Неверная длина номера")
            else:
                is_valid_phone = True
        except ValueError:
            print("Не валидный номер")
            continue
        except LenNumberError as err:
            print(err)
            continue
    return [first_name, last_name, phone_number]

def create_file(file):
    with open(file, "w", encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()

def read_file(file):
    with open(file, "r", encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)

def write_file(file, lst):
    res = read_file(file)
    for el in res:
        if el["Телефон"] == str(lst[2]):
            print("Такой телефон уже есть")
            return
    obj = {"Имя": lst[0], "Фамилия": lst[1], "Телефон": lst[2]}
    res.append(obj)
    with open(file, "w", encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)

def copy_file(f_obj, c_file, str_num):
    with open(c_file, "w", encoding='utf-8', newline='') as data:

        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerow(f_obj[str_num])
    print('Копирование выполнено успешно')

file_name = 'phone.csv'

def main():
    print("Доступные команды: r - чтение файла, w - создание и запись файла, с - копирование файла, q - выход из программы")
    while True:
        command = input("Введите команду: ")
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name, get_info())
        elif command == 'r':
            if not exists(file_name):
                print("Файл отсутствует")
                continue
            print(*read_file(file_name))
        elif command == 'c':
            file = input('Введите имя копируемого файла: ')
            if not exists(file):
                print("Файл отсутствует")
                continue
            obj_lst = read_file(file)  
            print(obj_lst)
            is_valid_str_num = False
            while not is_valid_str_num:
                try:
                    num_row = int(int(input("Введите номер копируемой строки: ")) - 1)
                    if not exists(num_row):
                        raise RowError("Заданный файл не содержит вводимую строку")
                    else:
                        is_valid_str_num = True
                except ValueError:
                    print("Не валидная строка")
                    continue
                except RowError as err:
                    print(err)
                    continue
            file_copy = input('Введите имя файла в который будете копировать: ')
            if not exists(file_copy):
                create_file(file_copy)
            copy_file(obj_lst, file_copy, num_row)

main()