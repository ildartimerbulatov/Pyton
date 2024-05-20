'''
Создать телефонный справочник с
возможностью импорта и экспорта данных в
формате .txt. Фамилия, имя, отчество, номер
телефона - данные, которые должны находиться
в файле.
1. Программа должна выводить данные
2. Программа должна сохранять данные в
текстовом файле
3. Пользователь может ввести одну из
характеристик для поиска определенной
записи(Например имя или фамилию
человека)
4. Использование функций. Ваша программа
не должна быть линейной
'''

from os.path import exists
from csv import DictReader, DictWriter

class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt

class NameError(Exception):
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
                raise NameError("Не валидная фамилия")
            else:
                is_valid_last_name = True
        except NameError as err:
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
            print("Не валидный номер!!!")
            continue
        except LenNumberError as err:
            print(err)
            continue

    return [first_name, last_name, phone_number]

def create_file(file_name):
    with open(file_name, "w", encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()

def read_file(file_name):
    with open(file_name, "r", encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)

def write_file(file_name, lst):
    if not exists(file_name):
        create_file(file_name)
    res = read_file(file_name)
    for el in res:
        if el["Телефон"] == str(lst[2]):
            print("Такой телефон уже есть")
            return

    obj = {"Имя": lst[0], "Фамилия": lst[1], "Телефон": lst[2]}
    res.append(obj)
    with open(file_name, "w", encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)

def search_by_name(file_name):
    name = input("Введите имя для поиска: ")
    data = read_file(file_name)
    found_records = [record for record in data if record["Имя"].lower() == name.lower()]
    if found_records:
        print("Найденные записи:")
        for record in found_records:
            print(f"Имя: {record['Имя']}, Фамилия: {record['Фамилия']}, Телефон: {record['Телефон']}")
    else:
        print("Записи не найдены.")

def search_by_surname(file_name):
    surname = input("Введите фамилию для поиска: ")
    data = read_file(file_name)
    found_records = [record for record in data if record["Фамилия"].lower() == surname.lower()]
    if found_records:
        print("Найденные записи:")
        for record in found_records:
            print(f"Имя: {record['Имя']}, Фамилия: {record['Фамилия']}, Телефон: {record['Телефон']}")
    else:
        print("Записи не найдены.")

def main():
    file_name = 'phone.txt'
    while True:
        print("\nДоступные команды:")
        print("w - Запись новой записи в файл")
        print("r - Вывод всех записей из файла")
        print("n - Поиск по имени")
        print("s - Поиск по фамилии")
        print("q - Выход из программы")

        command = input("Введите команду: ")

        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name, get_info())
        elif command == 'r':
            if not exists(file_name):
                print("Файл отсутствует. Создайте его")
                continue
            print(*read_file(file_name))
        elif command == 'n':
            search_by_name(file_name)
        elif command == 's':
            search_by_surname(file_name)
        else:
            print("Неверная команда. Попробуйте еще раз.")

if __name__ == "__main__":
    main()