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
    print(f"Файл {file_name} создан.")

def read_file(file_name):
    if not exists(file_name):
        create_file(file_name)
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
    print("Запись добавлена.")

def search_by_name(file_name):
    name = input("Введите имя для поиска: ")
    data = read_file(file_name)
    found_records = [record for record in data if record["Имя"].lower() == name.lower()]
    if found_records:
        print("Найденные записи:")
        print_records(found_records)
        return found_records
    else:
        print("Записи не найдены.")
        return []

def search_by_surname(file_name):
    surname = input("Введите фамилию для поиска: ")
    data = read_file(file_name)
    found_records = [record for record in data if record["Фамилия"].lower() == surname.lower()]
    if found_records:
        print("Найденные записи:")
        print_records(found_records)
        return found_records
    else:
        print("Записи не найдены.")
        return []

def update_record(file_name):
    print("Поиск записи для изменения:")
    found_records = search_by_name(file_name) + search_by_surname(file_name)
    if found_records:
        record_to_update = int(input("Введите номер записи для изменения: ")) - 1
        if 0 <= record_to_update < len(found_records):
            new_info = get_info()
            data = read_file(file_name)
            for record in data:
                if record == found_records[record_to_update]:
                    record['Имя'] = new_info[0]
                    record['Фамилия'] = new_info[1]
                    record['Телефон'] = new_info[2]
            with open(file_name, "w", encoding='utf-8', newline='') as data_file:
                f_writer = DictWriter(data_file, fieldnames=['Имя', 'Фамилия', 'Телефон'])
                f_writer.writeheader()
                f_writer.writerows(data)
            print("Запись обновлена.")
        else:
            print("Неверный номер записи.")

def delete_record(file_name):
    print("Поиск записи для удаления:")
    found_records = search_by_name(file_name) + search_by_surname(file_name)
    if found_records:
        record_to_delete = int(input("Введите номер записи для удаления: ")) - 1
        if 0 <= record_to_delete < len(found_records):
            data = read_file(file_name)
            data = [record for record in data if record != found_records[record_to_delete]]
            with open(file_name, "w", encoding='utf-8', newline='') as data_file:
                f_writer = DictWriter(data_file, fieldnames=['Имя', 'Фамилия', 'Телефон'])
                f_writer.writeheader()
                f_writer.writerows(data)
            print("Запись удалена.")
        else:
            print("Неверный номер записи.")

def print_records(records):
    for record in records:
        print(f"Имя: {record['Имя']}, Фамилия: {record['Фамилия']}, Телефон: {record['Телефон']}")

def main():
    file_name = 'phone.csv'
    if not exists(file_name):
        create_file(file_name)

    while True:
        print("\nДоступные команды:")
        print("w - Запись новой записи в файл")
        print("r - Вывод всех записей из файла")
        print("n - Поиск по имени")
        print("s - Поиск по фамилии")
        print("u - Изменение записи")
        print("d - Удаление записи")
        print("q - Выход из программы")

        command = input("Введите команду: ")

        if command == 'q':
            break
        elif command == 'w':
            write_file(file_name, get_info())
        elif command == 'r':
            if not exists(file_name):
                print("Файл отсутствует. Создайте его.")
                create_file(file_name)
            else:
                records = read_file(file_name)
                if records:
                    print_records(records)
                else:
                    print("Записей нет.")
        elif command == 'n':
            search_by_name(file_name)
        elif command == 's':
            search_by_surname(file_name)
        elif command == 'u':
            update_record(file_name)
        elif command == 'd':
            delete_record(file_name)
        else:
            print("Неверная команда. Попробуйте еще раз.")

if __name__ == "__main__":
    main()
