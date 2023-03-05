import json
import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()
    if base:
        print('Date base connected OK')

    base.execute(
        f'CREATE TABLE IF NOT EXISTS categories_db '
        f'(id INTEGER PRIMARY KEY AUTOINCREMENT, '
        f'name TEXT, color TEXT)'
    )

    base.execute(
        f'CREATE TABLE IF NOT EXISTS accounts_db '
        f'(id INTEGER PRIMARY KEY AUTOINCREMENT, '
        f'name TEXT, color TEXT, balance TEXT, currency TEXT)'
    )

    base.execute(
        f'CREATE TABLE IF NOT EXISTS savings_db '
        f'(id INTEGER PRIMARY KEY AUTOINCREMENT, '
        f'name TEXT, color TEXT, balance TEXT, goal TEXT, currency TEXT)'
    )

    base.execute(
        f'CREATE TABLE IF NOT EXISTS transaction_db '
        f'(id INTEGER PRIMARY KEY AUTOINCREMENT, '
        f'date TEXT, type TEXT, from_id TEXT, to_id TEXT, '
        f'from_SUM TEXT, from_currency TEXT, '
        f'to_SUM TEXT, to_currency TEXT, note TEXT)'
    )

    base.commit()


def accounts_db_read():
    accounts_data_dict = {}

    for row in cur.execute(f'SELECT * FROM accounts_db').fetchall():
        account_id = 'account_' + str(row[0])
        accounts_data_dict[account_id] = {
            'Name': row[1],
            'Color': json.loads(row[2]),
            'Balance': float(row[3]),
            'Currency': row[4]
        }

    return accounts_data_dict


def savings_db_read():
    savings_data_dict = {}

    for row in cur.execute(f'SELECT * FROM savings_db').fetchall():
        savings_id = 'savings_' + str(row[0])

        savings_data_dict[savings_id] = {
            'Name': row[1],
            'Color': json.loads(row[2]),
            'Balance': row[3],
            'Goal': row[4],
            'Currency': row[5]
        }

    return savings_data_dict


def categories_db_read():
    categories_data_dict = {}

    for row in cur.execute(f'SELECT * FROM categories_db').fetchall():
        category_id = 'Categories_' + str(row[0])
        categories_data_dict[category_id] = {
            'Name': row[1],
            'Color': json.loads(row[2])
        }

    return categories_data_dict


def transaction_db_read():
    transaction_dict = {}

    for row in cur.execute(f'SELECT * FROM transaction_db').fetchall():
        trans_id = row[0]

        transaction_dict[trans_id] = {}

        transaction_dict[trans_id]['Date'] = row[1]
        transaction_dict[trans_id]['Type'] = row[2]
        transaction_dict[trans_id]['From'] = row[3]
        transaction_dict[trans_id]['To'] = row[4]
        transaction_dict[trans_id]['FromSUM'] = row[5]
        transaction_dict[trans_id]['FromCurrency'] = row[6]
        transaction_dict[trans_id]['ToSUM'] = row[7]
        transaction_dict[trans_id]['ToCurrency'] = row[8]
        transaction_dict[trans_id]['Сomment'] = row[9]

    return transaction_dict

def transaction_db_write(trans_data_dict):
    cur.execute(f'INSERT INTO transaction_db '
                    f'(date, type, from_id, to_id, from_SUM, from_currency, to_SUM, to_currency, note) '
                    f'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (trans_data_dict['Date'], trans_data_dict['Type'], trans_data_dict['From'], trans_data_dict['To'],
                     trans_data_dict['FromSUM'], trans_data_dict['FromCurrency'], trans_data_dict['ToSUM'],
                     trans_data_dict['ToCurrency'], trans_data_dict['Comment'])
                    )
    base.commit()

def add_to_transaction_db(data_dict):
    for data_list in data_dict.values():
        cur.execute(f'INSERT INTO transaction_db '
                    f'(date, type, from_id, to_id, from_SUM, from_currency, to_SUM, to_currency, note) '
                    f'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (data_list['Date'], data_list['Type'], data_list['From'], data_list['To'],
                     data_list['FromSUM'], data_list['FromCurrency'], data_list['ToSUM'],
                     data_list['ToCurrency'], data_list['Comment'])
                    )

    base.commit()
