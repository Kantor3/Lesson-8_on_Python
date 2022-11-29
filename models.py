# Структура данных информационной системы "Сотрудники компании":
# Отдел:
import copy
from my_lib import *

FORMATS_file = ('csv', 'json', 'txt')       # Форматы файлов выгрузки / Загрузки

# Справочник "Сотрудники":
STAFFS_db = [{'id': 1, 'fio': 'Ivan Petrov', 'salary': 40},
             {'id': 2, 'fio': 'Bob Ivanov', 'salary': 50},
             {'id': 3, 'fio': 'John Don', 'salary': 100}
             ]
STRUCT_staffs = tuple(STAFFS_db[0].keys())
TYPE_staffs = tuple(map(type, STAFFS_db[0].values()))

# Справочник "Отделы":
DEPARTMENTS_db = [{'id': 10, 'name': 'accounting', 'staffs': [2, 1], 'manager': 1},
                  {'id': 11, 'name': 'marketing', 'staffs': [3], 'manager': 3}
                  ]
STRUCT_departments = tuple(DEPARTMENTS_db[0].keys())
TYPE_departments = tuple(map(type, DEPARTMENTS_db[0].values()))


# Добавление записей в БД
def add_db(records, db, structure, uniq=True):
    if not records: return None
    id_name = structure[0]
    add_records = []

    if not isinstance(records[0], dict):
        records = [dict([(k, v) for k, v in zip(structure[1:], record)]) for record in records]

    for record in records:  # Для каждой записи переданного пакета. Если запись уже с id - "отрезаем" ее
        record_short = record if len(record) < len(structure) else \
                       dict([el for el in tuple(record.items())[1:]])

        if uniq and where(record_short, db): continue  # добавляемая запись не может совпадать с к-л в БД

        key_record = record.keys()
        record_new = {id_name: get_uniqid_db(db, id_name=id_name)}  # первое поле - ключ записи (id)
        add_records.append(record_new)
        for k in structure[1:]:
            record_new[k] = record[k] if k in key_record else None  # Присваиваем None при отсутствии нужного поля
        db.append(record_new)

    return add_records


# Добавление новых сотрудников
def add_staffs(records):
    staffs_added = add_db(records, STAFFS_db, STRUCT_staffs) if records else None
    db_name = 'список "Сотрудники"'
    if staffs_added:
        return staffs_added, f'В {db_name} добавлены {len(staffs_added)} записей'
    else:
        return None, f'Нет записей для добавления в {db_name}'


# Добавление отделов
def add_departments(records):
    departments_added = add_db(records, DEPARTMENTS_db, STRUCT_departments) if records else None
    db_name = 'список "Отделы"'
    if departments_added:
        return departments_added, f'В {db_name} добавлены {len(departments_added)} записей'
    else:
        return None, f'Нет записей для добавления в {db_name}'


# Исключение в учете сотрудника из отдела
def exception(id_stuff):
    id_stuff = int(id_stuff)
    department_ex = None
    for ind, department in enumerate(DEPARTMENTS_db):
        department_src = copy.deepcopy(department)
        department['staffs'] = list(filter(lambda el: el != id_stuff, department['staffs']))
        if department['manager'] == id_stuff:                   department['manager'] = 0
        if department['staffs'] != department_src['staffs']:    department_ex = department
        if department != department_src:                        DEPARTMENTS_db[ind] = department
    return department_ex


# Включение в учете сотрудника в отдел
def inclusion(id_stuff, id_department):
    ind_department = where(id_department, DEPARTMENTS_db)
    dep_staffs = set(DEPARTMENTS_db[ind_department]['staffs'])
    dep_staffs.add(id_stuff)
    DEPARTMENTS_db[ind_department]['staffs'] = list(dep_staffs)


# Перемещение сотрудника в другой отдел
def move_staff(who_where):
    if not who_where:
        return None, 'Операция перемещения сотрудника в др.отдел отменена'

    id_stuff, id_department = map(int, who_where)
    ind_stuff = where(id_stuff, STAFFS_db)
    ind_department = where(id_department, DEPARTMENTS_db)
    if ind_stuff is None or ind_department is None:
        return None, f'Сотрудник и/или отдел c кодами [{id_stuff}] и [{id_department}] соответственно, в БД не найдено'
    else:
        exception(id_stuff)                 # в учете: исключение сотрудника из прежнего отдела (если он там учтен)
        inclusion(id_stuff, id_department)  # в учете: включение сотрудника в новый отдел
        return True, f'Сотрудник {STAFFS_db[ind_stuff]} перемещен в отдел {DEPARTMENTS_db[ind_department]}'


# Увольнение сотрудника
def dismissal(id_):
    ind = where(id_, STAFFS_db)
    staff = STAFFS_db[ind]
    STAFFS_db.pop(ind)                         # Удаление из списка "Сотрудники"
    department = exception(id_)
    return True, f'Сотрудник {staff} уволен из отдела {department}'


# Обновление базы данных загруженными данными
def updating_db(result_loads):

    global STAFFS_db
    global DEPARTMENTS_db

    load_staffs, load_departments = tuple(result_loads)

    """ -------- Это не прошло! -----------------------
    # Не удалось таким способом заменить (загрузить) новые данные в глобальные переменные
    # STAFFS_db       = copy.deepcopy(load_staffs[0])
    # DEPARTMENTS_db  = copy.deepcopy(load_departments[0])
    """

    STAFFS_db.clear()
    DEPARTMENTS_db.clear()
    [STAFFS_db.append(el) for el in load_staffs[0]]
    [DEPARTMENTS_db.append(el) for el in load_departments[0]]

    return result_loads
