import os.path as os
from models import *
import ui.ui_controller as c

MENU_NAME = 'Меню системы'
MENU_DELINEATION = '-' * (len(MENU_NAME) + 1)


# Вывести меню.
# Вывести приглашение к выбору пункта меню
# Собственно выбор меню
def menu():
    print()
    print(f'{MENU_NAME}:')
    print(MENU_DELINEATION)
    for key, item in c.MENU_ACTIONS.items():
        print(f'{key}  {item[0]}')
    print(MENU_DELINEATION)
    print()

    items = tuple(map(str, c.MENU_ACTIONS.keys()))
    inp = get_input(items, type_input=tuple, txt='Выберите пункт меню (укажите номер)\n', not_mess=None)

    return int(inp) if inp else None


# Вывод сообщений (уведомлений) о результатах выполнения операций, подсказок и пр.
def output_not(title_not, content_not=None):
    pointer = '---->'
    print()
    mark = ':' if content_not else '!'
    print(f'{pointer} {title_not}{mark}')
    if content_not:
        for line in content_not:
            print(f'{" "*len(pointer)}{line}')


# Вывести переданный список записей БД в формате отчета
def output_report(records, structure_db=None, txt='База данных'):

    if not records:
        if not structure_db:
            return None, f'Список записей {txt} пуст!'
        records = [dict([(k, None) for k in structure_db])]

    l_keys = tuple(records[0].keys())
    l_max_val = get_maxlen_fields(records)
    outline = '-' * (sum(l_max_val) + 3)
    print('\n', txt)
    print(outline)
    print(*[e.ljust(l) for e, l in zip(l_keys, l_max_val)])
    print(outline)
    records_prn = [tuple([str(e).ljust(l) for e, l in zip(tuple(rec.values()), l_max_val)]) for rec in records]
    for record in records_prn:
        print(*record)                              # Печать содержимого текущей записи
    print(outline)

    return l_max_val, None


# 1. Вывести Список отделов
def show_departments(operation=None):
    if operation: pass
    result, err_txt = output_report(DEPARTMENTS_db, structure_db=STRUCT_departments, txt='Список отделов:', )
    if not result:
        print(f'\n{err_txt}')


# 2. Вывести Список сотрудников
def show_staffs(operation=None):
    if operation: pass
    result, err_txt = output_report(STAFFS_db, structure_db=STRUCT_staffs, txt='Список сотрудников:')
    if not result:
        print(f'\n{err_txt}')


# 3. Вывести Список сотрудников отдела
def show_staffs_in_department(operation=None):
    if operation: pass
    ids = tuple(map(str, get_ids(DEPARTMENTS_db)))
    department_id = get_input(ids, type_input=tuple, default=ids[0], txt='Введите код отдела:', end='-')
    if department_id:
        department = DEPARTMENTS_db[where(int(department_id), DEPARTMENTS_db)]
        staffs_id = department['staffs']
        staffs_department = [STAFFS_db[where(id_, STAFFS_db)] for id_ in staffs_id]
        result, err_txt = output_report(staffs_department, txt=f'Список сотрудников отдела [{department["name"]}]:')
        if not result:
            print(f'\n{err_txt}')
    else:
        return None, 'Список сотрудников отдела пуст!'


# Ввод данных записей для добавления в базу данных
def input_records(operation, structure_db, types_fields):
    txt_for = c.MENU_ACTIONS[operation][0]
    structure_short = structure_db[1:]
    records_add = []
    print()
    while True:
        print(f'Для "{txt_for}" последовательно заполните значения полей {structure_short}:')
        for_input = tuple([el for el in structure_short])
        record = get_inputs(*for_input, type_input=str, not_mess=True, all_input=True)
        if empty_coll(record):
            print('Введена пустая запись')
        else:
            record = init_fields_none(record, types_fields)
            records_add.append(record)
        if check_exit(sign='+', txt_req='"+" - добавить запись, любая другая клавиша - завершить ввод -> ',
                      not_mess=True):
            break
    return records_add


# 4. Добавление сотрудников
def input_staffs(operation=None):
    staffs_add = input_records(operation, STRUCT_staffs, TYPE_staffs[1:])
    return staffs_add


# 5. Добавление отдела (ов)
def input_departments(operation=None):
    departments_add = input_records(operation, STRUCT_departments, TYPE_departments[1:])
    return departments_add


# 6. Выбрать сотрудника и отдел, куда переместить сотрудника (вводом их id)
def select_who_where(operation=None):
    txt_for = c.MENU_ACTIONS[operation][0]
    print()
    print(f'Для выполнения операции "{txt_for}" введите код сотрудника и код отдела:')
    ids_staffs      = tuple(map(str, get_ids(STAFFS_db)))
    ids_departments = tuple(map(str, get_ids(DEPARTMENTS_db)))
    while True:
        for_input = ((ids_staffs, f'{STRUCT_staffs[0]} сотрудника "кого".'),
                     (ids_departments, f'{STRUCT_departments[0]} отдела "куда".'))
        ids = get_inputs(*for_input, type_input=tuple, not_mess=True)
        if not ids:                                     # Данные для выполнения операции не определены
            if check_exit(txt_req='Повторить ввод? ("y" - ДА) -> ', not_mess=True):
                return None
        else:
            return list(ids)


# 7. Выбрать сотрудника (вводом его id), например для его увольнения
def select_who(operation=None):
    txt_for = c.MENU_ACTIONS[operation][0]
    print()
    print(f'Для выполнения операции "{txt_for}" введите код сотрудника:')
    while True:
        ids = tuple(map(str, get_ids(STAFFS_db)))
        id_staff = get_input(ids, type_input=tuple, default=ids[0], txt='Введите код сотрудника:', end='-')
        if not id_staff:                                # Данные для выполнения операции не определены
            if check_exit(txt_req='Повторить ввод? ("y" - ДА) -> ', not_mess=True):
                return None
        else:
            return id_staff


# 8. Выбор формата файла - выгрузки (CSV, txt или JSON)
def select_format(available=None, default=None):
    print()
    format_sel = get_input(available, default=default, type_input=tuple,
                           txt='Выберите формат выгрузки данных', end='-q')
    return format_sel


# 9. Задание параметров загрузки (импорта)
# Задание имени файла загрузки
# Todo: То что ниже, пока не реализовано. Просто загрузка данных с диска сверху базы данных в оперативной памяти
#       позже можно это все расширить, как было сделано в задачи к Семинару 7.
#       Выбор способа импорта (загрузки) данных в справочник (только измененные, добавление только новых, все)
#       method - метод загрузки:
#               "-n" - только новые контакты
#               "-u" - только обновление изменений, имеющихся в базе, контактов
#               "-f" - как можно полное обновление
def set_load_param(def_method=None, def_namefile=None):    # method = '-r' - поверх данных, метод - замещение
    print()
    # Уточнение метода загрузки:
    if not def_method:
        methods = sep_option('nufr')
        print('Поддерживаются сл. методы загрузки:\n'
              '     "-n" - только новые контакты\n'
              '     "-u" - только обновление изменений, имеющихся в базе, контактов\n'
              '     "-f" - обновить, что можно, по максимуму \n'
              '     "-r" - полностью заместить данные загруженными')
        method = get_input(methods, default='-f', type_input=tuple,
                           txt='Введите способ загрузки данных', end='-q')
    else:
        method = def_method

    # Уточнение имени файла-загрузки:
    if not def_namefile:
        while True:
            filename = get_input(type_input=str, default='db.csv',
                                 txt='Введите имя файла загрузки (вместе с расширением)', end='-q')
            if filename is None: return None, 'Отменено пользователем'
            if not os.isfile(filename):
                print(f'Указанный файл {filename} не найден. Уточните имя.')
                continue
            break
    else:
        filename = def_namefile

    return filename, method
