import os
import json
from strings import FILEPATH


class DataStorage:
    def __init__(self):
        pass

    def save_number(self, number: dict):
        """
        Сохраняет запись в файл
        :param number: Данные записи
        :return:
        """
        if number is not None:
            if not self.check_file():
                json_string = json.dumps([number], indent=4)
            else:
                a = self.load_numbers()
                self.repair_file(a)
                a.append(number)
                json_string = json.dumps(a, indent=4)
            with open(FILEPATH, "w") as f:
                f.write(json_string)

    def load_numbers(self) -> list[dict[str, str]]:
        """
        Получает все записи из файла
        :return: Данные записей
        """
        if not self.check_file():
            return []
        else:
            with open(FILEPATH, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []

    def delete_number(self, number: dict):
        """
        Удаляет определенную запись из файла с записями
        :param number: Запись которую требуется удалить
        :return:
        """
        data = self.load_numbers()
        if number in data:
            data.remove(number)
        json_string = json.dumps(data)
        with open(FILEPATH, "w") as f:
            f.write(json_string)

    def check_file(self) -> bool:
        """
        Проверяет наличие файла в каталоге
        :return:
        """
        return os.path.exists(FILEPATH)

    def repair_file(self, data: list) -> list:
        """
        Удаляет некорректные записи в файле
        :param data: Список с неправильными записями
        :return: Исправленный список записей
        """
        for i in data:
            if i is None:
                data.remove(i)
        return data
