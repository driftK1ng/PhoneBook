from strings import *


def show_message(msg: str):
    """
    Выводит сообщение в терминал
    :param msg: Сообщение
    :return:
    """
    print(msg)


def show_numbers(data: list[dict]):
    """
    Выводит номера в консоль
    :param data: Список словарей записей
    :return:
    """
    for i in data:
        print(i["name"], i["surname"], i["middle_name"])
        print(f'{USER_INPUT_FIELDS["personal_number"].capitalize()}: {i["personal_number"]}')
        print(f'{USER_INPUT_FIELDS["work_number"].capitalize()}: {i["work_number"]}')
        print("==========================")


def show_help():
    """
    Выводит помощь в консоль
    :return:
    """
    print(SHORT_HELP_COMMANDS)


def show_change_help():
    """
    Выводить помощь в интерфейсе изменения
    :return:
    """
    print(CHANGE_INTERFACE_HELP)


def get_max_len(number: dict) -> int:
    """
    Вычисляет максимальную длину поля записи
    :param number: Запись номера
    :return: Максимальная длина
    """
    max_len = -1
    for item in number:
        if len(item) > max_len:
            max_len = len(item)
    return max_len


def show_difference(old_version: dict, new_version: dict):
    """
    Выводит разницу между старой и новой версией записи
    :param old_version: Старая версия записи
    :param new_version: Новая версия записи
    :return:
    """
    max_len = get_max_len(old_version)
    for item in old_version.keys():
        if old_version[item] == new_version[item]:
            arrow = ""
        else:
            arrow = "-->"
        print(f"{(USER_INPUT_FIELDS[item] + ':').ljust(15)}"
              f" {old_version[item].ljust(max_len)}\t{arrow}\t{new_version[item]}")
