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


def add_to_savings_db(data_dict):
    for data_list in data_dict.values():
        color = json.dumps(data_list['Color'])

        cur.execute(f'INSERT INTO savings_db (name, color, balance, goal, currency) VALUES (?, ?, ?, ?, ?)',
                    (data_list['Name'], color, data_list['Balance'], None, data_list['Currency']))

    base.commit()
