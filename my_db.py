import sqlite3


def openclose_db(func):
    # Декоратор для функций работы с базой данных
    def wrapper(base_name, *args, **kwargs):
        connect = sqlite3.connect(base_name)
        cursor = connect.cursor()
        return_value = func(cursor, *args, **kwargs)
        connect.commit()
        connect.close()
        return return_value
    return wrapper


def create_db(base_name: str, spisok: list):
    # Создание таблицы базы данных, на основании полученного списка из парсинга эксель файла.
    # На входе имя базы данных и список загрузки
    connect = sqlite3.connect(base_name)
    cursor = connect.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS dis (contract, counterparty, city, point, street, house, tp)')
    sqlite_insert_query = """INSERT INTO dis
                                 (contract, counterparty, city, point, street, house, tp)
                                 VALUES (?, ?, ?, ?, ?, ?, ?);"""
    cursor.executemany(sqlite_insert_query, spisok)
    connect.commit()
    connect.close()


@openclose_db
def search_by_contract(cursor, contract: str):
    # Функция поиска по лицевому счету base_name: str,
    results = cursor.execute(f"SELECT * FROM dis WHERE contract LIKE '%{contract}%'").fetchall()
    return results


@openclose_db
def search_by_counterparty(cursor, counterparty: str):
    # функция поиска по ФИО, наименованию
    results = cursor.execute(f"SELECT * FROM dis WHERE counterparty LIKE '%{counterparty}%'").fetchall()
    return results


@openclose_db
def search_by_address(cursor, address: list):
    # Функция поиска по адресу, как полному так и неполному.
    # В случае неполного адреса выдаются выборка подпадающие под условия
    for i in range(len(address)):   # Цикл проверяет, что в адресе есть символы и заменяет их пустой строкой
        if not address[i].isalnum():
            address[i] = ''
    results = cursor.execute(f"SELECT * FROM dis WHERE (city like '%{address[0]}%' or point like '%{address[0]}%') "
                             f"and street like '%{address[1]}%' and house like '%{address[2]}%'").fetchall()
    return results


@openclose_db
def search_by_tp(cursor, tp: str):
    # Функция поиска по ТП
    results = cursor.execute(f"SELECT * FROM dis WHERE tp LIKE '%{tp}%'").fetchall()
    return results


@openclose_db
def add_to_bd(cursor, newdis: list):
    # Добавляет нового отключенного в базу данных
    for i in range(len(newdis)):
        newdis[i] = newdis[i].lower()
    cursor.execute("INSERT INTO dis VALUES (?, ?, ?, ?, ?, ?, ?);",
                   (newdis[0], newdis[1], newdis[2], newdis[2], newdis[3], newdis[4], newdis[5]))


@openclose_db
def delete_from_bd(cursor, cont: str):
    # Удаление строки с отключенным из базы данных
    cursor.execute(f"DELETE from dis where contract LIKE '%{cont}%'")
