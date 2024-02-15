from saver import DataStorage
from strings import *
import view
import interface


def is_number(number: str) -> bool:
    """
    Проверяет состоит ли номер из чисел или нет
    :param number: Номер
    :return:
    """
    if number.startswith("+"):
        number = number[1:-1]
    return number.isdigit()


def correct_length(number: str) -> bool:
    """
    Проверяет что номер длинее 10 символов и короче 16 символов
    :param number: Номер
    :return:
    """
    return 10 < len(number) < 16


def make_number_from_data(data: list) -> dict:
    """
    Конвертирует список с данными записи в конечную запись для сохранения
    :param data: Обработанные данные пользователя
    :return: Готовый список данных о номере
    """
    fields: list = list(USER_INPUT_FIELDS.keys())
    number_data: dict = {}
    if not is_number(data[0]):
        data[0] = ""
    if not is_number(data[1]):
        data[1] = ""
    for i in range(len(fields)):
        if data[i] == "-":
            number_data[fields[i]] = ""
        else:
            number_data[fields[i]] = data[i]
    return number_data


def parse_input(command: str) -> list[str]:
    """
    Конвертирует команду пользователя в обработанные данные для дальнейших действий
    :param command: Команда пользователя
    :return: Обработанные данные
    """
    raw_data: list = command.split()
    raw_data.pop(0)
    return raw_data


def build_strong_query(query: list) -> dict[str, str]:
    """
    Формирует словарь аргументов по которым будет проходить поиск
    :param query: Список аргументов для формирования списка
    :return: Словарь аргументов
    """
    fields: list = list(USER_INPUT_FIELDS.keys())
    strong_query: dict = {}
    for i in range(len(query)):
        if query[i] != "-":
            strong_query[fields[i + 2]] = query[i]
    return strong_query


class Controller:
    __dataStorage: DataStorage

    def __init__(self):
        self.__dataStorage = DataStorage()
        view.show_message(HELP_MSG)
        interface.menu_interface(self)

    def check_number_in_file(self, personal_number, work_number):
        """
        Проверяет есть ли введённые номера в файле
        :param personal_number: Личный номер
        :param work_number: Рабочий номер
        :return:
        """
        for item in self.__dataStorage.load_numbers():
            if item["personal_number"] == personal_number or item["personal_number"] == work_number:
                return True
            elif item["work_number"] == personal_number or item["work_number"] == work_number:
                return True
        return False

    def add_number(self, number: dict):
        """
        Добавляет данные о номере в текстовый файл
        :param number: данные о номере
        :return:
        """
        self.__dataStorage.save_number(number)

    def delete_number(self, number: dict):
        """
        Удаляет номер из файла
        :param number: Номер для удаления
        :return:
        """
        self.__dataStorage.delete_number(number)

    def change_number(self, old_version: dict, new_version: dict):
        """
        Удаляет старую версию записи из файла и добавляет новую версию записи в файл
        :param old_version: Старая версия записи
        :param new_version: Новая версия записи
        :return:
        """
        self.delete_number(old_version)
        if self.check_number_data(list(new_version.values())):
            self.add_number(new_version)
            view.show_message(SUCCESS_CHANGE_MSG)
            return True
        else:
            self.add_number(old_version)
            view.show_message(BAD_INPUT_MSG)
            return False

    def search_numbers(self, number="", strong_query: dict[str, str] = None) -> list[dict[str, str]]:
        """
        Ищет номера либо по номеру либо по набору ФИО
        :param number: номер телефона
        :param strong_query: набор ФИО
        :return: Список найденных номеров
        """
        result: list[dict[str, str]] = []
        if number != "":
            data: list[dict[str, str]] = self.__dataStorage.load_numbers()
            for item in data:
                if item["personal_number"].find(number) != -1 or item["work_number"].find(number) != -1:
                    result.append(item)
        elif strong_query is not None:
            data = self.__dataStorage.load_numbers()
            for item in data:
                flag = True
                for category in strong_query.keys():
                    if item[category] != (strong_query[category]):
                        flag = False
                if flag:
                    result.append(item)
        return result

    def select_numbers(self, command) -> list[dict[str, str]]:
        """
        Проверяет правильность введенной команды и вызывает функцию для поиска записей
        :param command: Запрос пользователя
        :return: Список отобранных записей
        """
        query: list[str] = parse_input(command)
        if len(query) > 0:
            for item in query:
                if is_number(item):
                    return self.search_numbers(number=item)
            return self.search_numbers(strong_query=build_strong_query(query))
        return []

    def show_numbers(self, size=-1, page=0):
        """
        Предоставляет интерфейс просмотра страниц и выводит записи
        :param size: Определяет размер страницы
        :param page: Определяет страницу для вывода
        :return:
        """
        data: list[dict[str, str]] = self.__dataStorage.load_numbers()
        if size < 0:
            view.show_numbers(data)
        else:
            if page > 0:
                page -= 1
            numbers: list[dict[str, str]] = data[0 + size * page:size + size * page]
            if len(numbers) > 0:
                view.show_message(SHOW_INTERFACE_MSG)
                view.show_numbers(data[0 + size * page:size + size * page])
                interface.show_interface(self, size, page)

    def request_show_numbers(self, command):
        """
        Запрашивает данные из файла и отправляет эти данные на вывод
        :return:
        """
        data: list[str] = parse_input(command)
        if len(data) > 0:
            try:
                if data[0] == "-s" and data[1].isdigit():
                    try:
                        if data[2] == '-p' and data[3].isdigit():
                            self.show_numbers(int(data[1]), int(data[3]))
                    except IndexError:
                        self.show_numbers(int(data[1]))
            except IndexError:
                view.show_message(BAD_INPUT_MSG)
        else:
            self.show_numbers()

    def request_selected_numbers(self, command: str):
        """
        Выводит в консоль выборку записей
        :param command: Команда пользователя
        :return:
        """
        view.show_numbers(self.select_numbers(command))

    def request_change_number(self, command: str):
        """
        Поиск записи и открытие интерфейса для редактирования записи
        :param command: Команда пользователя
        :return:
        """
        result: list[dict[str, str]] = self.select_numbers(command)
        if len(result) > 1:
            view.show_message(MORE_THAN_ONE_MSG)
            view.show_numbers(result)
        elif len(result) == 1:
            view.show_numbers(result)
            interface.change_interface(self, result[0])
        else:
            view.show_message(BAD_SELECT_MSG)

    def request_add_number(self, command: str):
        """
        Обрабатывает ввод пользователя и добавляет запись в файл
        :param command:
        :return:
        """
        data: list[str] = parse_input(command)
        if self.check_number_data(data):
            view.show_message(SUCCESS_INPUT_MSG)
            self.add_number(make_number_from_data(data))

    def check_number_data(self, data: list) -> bool:
        """
        Проверяет содержит ли список все элементы для сохранения номера
        :param data: Обработанный ввод пользователя
        :return:
        """
        if len(data) == 5:
            if data[0] == data[1]:
                view.show_message(EQUALS_NUMBERS_MSG)
                return False
            elif not (is_number(data[0]) or is_number(data[1])):
                view.show_message(EMPTY_NUMBERS_MSG)
                return False
            elif not (correct_length(data[0]) or correct_length(data[1])):
                view.show_message(EMPTY_NUMBERS_MSG)
                return False
            elif self.check_number_in_file(data[0], data[1]):
                view.show_message(EXISTS_NUMBERS_MSG)
                return False
            elif data[2] == "-" and data[3] == "-" and data[4] == '-':
                view.show_message(NO_NAME_MSG)
                return False
            return True
        view.show_message(BAD_INPUT_MSG)
        return False

    def request_delete_number(self, command: str):
        """
        Отправка запроса модулю для удаления записи из файла
        :param command:
        :return:
        """
        result: list[dict[str, str]] = self.select_numbers(command)
        if len(result) == 1:
            self.__dataStorage.delete_number(result[0])
            view.show_message(SUCCESS_DELETE_MSG)
        elif len(result) > 1:
            view.show_numbers(result)
            view.show_message(MORE_THAN_ONE_MSG)
        else:
            view.show_message(BAD_SELECT_MSG)

    def request_help(self, command: str):
        """
        Определяет какой пункт помощи вывести в консоль
        :param command: Команда пользователя
        :return:
        """
        try:
            help_category: str = command.split(" ")[1]
            try:
                view.show_message(INPUT_HELP_COMMANDS[help_category])
            except KeyError:
                view.show_message(BAD_INPUT_MSG)
        except IndexError:
            view.show_help()
