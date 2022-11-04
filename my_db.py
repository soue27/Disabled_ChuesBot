import sqlite3


global connect, cursor


def open_db():
    global connect, cursor
    connect = sqlite3.connect('disabled.sqlite3')
    cursor = connect.cursor()
    if connect:
        print('База данных подключена')
    else:
        print('Необходимо добавить базу данных')



async def create_db(base_name: str, spisok: list):
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


def search_by_contract(contract: str):
    # Функция поиска по лицевому счету base_name: str,
    results = cursor.execute(f"SELECT * FROM dis WHERE contract LIKE '%{contract.lower()}%'").fetchall()
    return results


def search_by_counterparty(counterparty: str):
    # функция поиска по ФИО, наименованию
    results = cursor.execute(f"SELECT * FROM dis WHERE counterparty LIKE '%{counterparty.lower()}%'").fetchall()
    return results


def search_by_address(adres: str):
    # Функция поиска по адресу, как полному так и неполному.
    # В случае неполного адреса выдаются выборка подпадающие под условия
    adres = adres.replace(' ', '')
    address = adres.split(',')
    for i in range(len(address)):   # Цикл проверяет, что в адресе есть символы и заменяет их пустой строкой для работы фильтра
        if not address[i].isalnum():
            address[i] = ''
    results = cursor.execute(f"SELECT * FROM dis WHERE (city like '%{address[0].lower()}%' or point like '%{address[0].lower()}%') "
                             f"and street like '%{address[1].lower()}%' and house like '%{address[2].lower()}%'").fetchall()
    return results


def search_by_tp(tp: str):
    # Функция поиска по ТП
    results = cursor.execute(f"SELECT * FROM dis WHERE tp LIKE '%{tp}%'").fetchall()
    return results


def add_to_bd(newdis: list):
    # Добавляет нового отключенного в базу данных
    for i in range(len(newdis)):
        newdis[i] = newdis[i].lower()
    cursor.execute("INSERT INTO dis VALUES (?, ?, ?, ?, ?, ?, ?);",
                   (newdis[0], newdis[1], newdis[2], newdis[2], newdis[3], newdis[4], newdis[5]))


def delete_from_bd(cont: str):
    # Удаление строки с отключенным из базы данных
    cursor.execute(f"DELETE from dis where contract LIKE '%{cont}%'")
