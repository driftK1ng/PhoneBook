import view
from strings import MENU_INTERFACE_MSG, PAGE_INTERFACE_MSG, CHANGE_INTERFACE_MSG, HELP_MSG, BAD_INPUT_MSG


def menu_interface(controller):
    """
    Предоставляет возможность ввода комманд в терминал
    :param controller: Контроллер вызывающий данный метод
    :return:
    """
    while True:
        view.show_message(MENU_INTERFACE_MSG)
        command: str = input()
        if command.startswith("insert "):
            controller.request_add_number(command)
        elif command.startswith("search "):
            controller.request_selected_numbers(command)
        elif command.startswith("change "):
            controller.request_change_number(command)
        elif command.startswith("show ") or command == "show":
            controller.request_show_numbers(command)
        elif command.startswith("delete "):
            controller.request_delete_number(command)
        elif command.startswith("help ") or command == "help":
            controller.request_help(command)


def change_interface(controller, old_version: dict):
    """
    Предоставляет возможность ввода данных для изменения
    :param controller: Контроллер вызывающий данную функцию
    :param old_version: Запись, которая будет изменяться
    :return:
    """
    fields = list(old_version.keys())
    new_version: dict[str, str] = old_version.copy()
    view.show_message(HELP_MSG)
    while True:
        view.show_message(CHANGE_INTERFACE_MSG)
        data = input()
        if data == "enter" and controller.change_number(old_version, new_version):
            break
        elif data == "0":
            break
        elif data == "help":
            view.show_change_help()
        elif len(data.split()) == 5:
            data = data.split()
            for i in range(len(data)):
                if data[i] == "-":
                    new_version[fields[i]] = old_version[fields[i]]
                elif data[i] == "DELETE":
                    new_version[fields[i]] = ""
                else:
                    new_version[fields[i]] = data[i]
            view.show_difference(old_version, new_version)
        else:
            view.show_message(BAD_INPUT_MSG)


def show_interface(controller, size: int, page: int):
    """
    Показывает интерфейс для просмотра страниц
    :param controller: Контроллер вызвавший эту функцию
    :param size: Размер страницы
    :param page: Текущая страница
    :return:
    """
    view.show_message(PAGE_INTERFACE_MSG)
    command: str = input()
    if command != "0":
        controller.show_numbers(size, page + 2)
