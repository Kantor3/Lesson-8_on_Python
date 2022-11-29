from .ui_view import *
from loads import *

MENU_ACTIONS = {
    1: ['Вывести список отделов', show_departments],
    2: ['Вывести список всех сотрудников', show_staffs],
    3: ['Вывести список сотрудников отдела', show_staffs_in_department],
    4: ['Добавить сотрудника', input_staffs, add_staffs],
    5: ['Добавить отдел', input_departments, add_departments],
    6: ['Переместить сотрудника в другой отдел', select_who_where, move_staff],
    7: ['Уволить сотрудника', select_who, dismissal],
    8: ['Выгрузить данные на диск', save_db],
    9: ['Загрузить данные в БД', load_db, updating_db],
    0: ['Выход', lambda: None]
}


def main():
    select_item = None

    while select_item is None or select_item:
        select_item = menu()
        if select_item is None:
            print('Не выбрано ничего. Укажите цифру меню ...')
            continue

        if not select_item:
            if check_exit(txt_req='Завершить работу с программой? ("y" - ДА) -> ', enter=False):
                break
            else:
                select_item = None
                continue

        print(f'выбран пункт {select_item} - [{MENU_ACTIONS[select_item][0]}]')
        input_data = MENU_ACTIONS[select_item][1](select_item)

        if input_data:                             # если 1-й метод возвращает данные для 2-го метода
            if isinstance(input_data, tuple):      # если данные не список, операция на этом завершена
                returns = input_data
            else:                                  # иначе - запускаем переданный метод, в который
                returns = MENU_ACTIONS[select_item][2](input_data)  # передаем полученные данные
        else:
            returns = input_data, None

        returns = returns if isinstance(returns[0], tuple) else (returns, )
        for result, message in returns:
            if message:
                details = None if isinstance(result, (type(None), bool)) else result
                output_not(message, content_not=details)

        input("\nPress Enter to continue... ")
