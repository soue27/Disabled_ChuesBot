import xlrd
import os


def migration_xls_sqllite(filename: str):
    # договор, контрагент, город ту, нас. пункт ту, улица ту, дом ту, тп
    table = [0, 0, 0, 0, 0, 0, 0]
    stroka = []
    spisok = []
    book = xlrd.open_workbook(filename, logfile=open(os.devnull, 'w'))
    sheet = book.sheet_by_index(0)
    for i in range(sheet.ncols):
        if sheet.cell(0, i).value.lower() == 'договор':
            table[0] = i
        elif sheet.cell(0, i).value.lower() == 'контрагент':
            table[1] = i
        elif sheet.cell(0, i).value.lower() == 'город ту':
            table[2] = i
        elif sheet.cell(0, i).value.lower() == 'нас. пункт ту':
            table[3] = i
        elif sheet.cell(0, i).value.lower() == 'улица ту':
            table[4] = i
        elif sheet.cell(0, i).value.lower() == 'дом ту':
            table[5] = i
        elif sheet.cell(0, i).value.lower() == 'тп':
            table[6] = i
    for i in range(1, sheet.nrows-1):
        for j in table:
            stroka.append(sheet.cell(i, j).value.lower())
        korteg = tuple(stroka)
        spisok.append(korteg)
        stroka = []
    return spisok
