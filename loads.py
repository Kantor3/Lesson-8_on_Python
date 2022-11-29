import csv
# from my_lib import *
from models import *
from ui.ui_view import select_format, set_load_param


# Собственно выгрузка БД и запись на диск
def unload_db(db, format_file, file_name=None):

    if not len(db): return None, 'База данных пустая'

    full_name = f'{"db" if file_name is None else file_name}.{format_file}'
    with open(full_name, mode="w", encoding='utf-8') as file:  # encoding='utf-8'
        names = [*DEPARTMENTS_db[0].keys(), *STAFFS_db[0].keys()]
        file_wr = csv.DictWriter(file, delimiter=",", lineterminator="\r", fieldnames=names)
        file_wr.writeheader()
        file_wr.writerows(db)

    return full_name, None


# 8. Выгрузка БД
# todo: Запрос объема для выгрузки базы (отбор записей для выгрузки все или запрошенные)
#       Реализовать остальные форматы файлов-выгрузки из перечня [FORMATS_file]
def save_db(operation=None):

    if operation is None: pass                                    # для единообразия вызова

    form = FORMATS_file[0]
    format_file = select_format(available=form, default=form)     # - пока ограничимся CSV-форматом
    if not (format_file is None):
        db = [*DEPARTMENTS_db, *STAFFS_db]
        res, txt_error = unload_db(db, format_file, )
        message = f'Выгрузка в файл "{res}" выполнена успешно!' if res else \
                  f'Выгрузка в файл не состоялась. Error: {txt_error}'
    else:
        message = 'Формат файла выгрузки не определен. Выгрузка в файл не состоялась. Error: [0]'

    return message, None


# 9. Загрузка БД
def load_db(operation=None):

    if operation is None: pass  # заглушка - для единообразия вызова

    filename, method = set_load_param(def_method='-r', def_namefile='db.csv')
    if method: pass             # заглушка - пока не используется
    db_load = []

    with open(filename, mode="r", encoding='utf-8') as file:

        file_rd = csv.DictReader(file, delimiter=",")
        for row in file_rd:
            db_load.append(row)

    # Отделяем список Сотрудников
    db_temp = get_fill_fields(db_load, STRUCT_staffs[1:])
    db_temp = slice_by_fields(db_temp, STRUCT_staffs)
    staffs_in = typing_by_fields(db_temp, (STRUCT_staffs, TYPE_staffs))
    result_load1 = (staffs_in, 'Загружены справочник "Сотрудники"')

    # Отделяем список Отделов
    db_temp = get_fill_fields(db_load, STRUCT_departments[1:])
    db_temp = slice_by_fields(db_temp, STRUCT_departments)
    departments_in = typing_by_fields(db_temp, (STRUCT_departments, TYPE_departments))
    result_load2 = (departments_in, 'Загружены справочник "Отделы"')

    results = [result_load1, result_load2]
    return results
