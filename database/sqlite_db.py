import json
import sqlite3 as sq


def sql_start() -> None:
    global base, cur
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()
    if base:
        print('Date base connected OK')

    # categories_db
    base.execute(
        f'CREATE TABLE IF NOT EXISTS categories_db '
        f'(id INTEGER PRIMARY KEY AUTOINCREMENT, '
        f'name TEXT, color TEXT, icon TEXT)'
    )

    base.execute(
        f'CREATE TABLE IF NOT EXISTS incomes_db '
        f'(id INTEGER PRIMARY KEY AUTOINCREMENT, '
        f'name TEXT, color TEXT, icon TEXT)'
    )

    # accounts_db
    base.execute(
        f'CREATE TABLE IF NOT EXISTS accounts_db '
        f'(id INTEGER PRIMARY KEY AUTOINCREMENT, '
        f'name TEXT, color TEXT, balance TEXT, currency TEXT)'
    )

    # savings_db
    base.execute(
        f'CREATE TABLE IF NOT EXISTS savings_db '
        f'(id INTEGER PRIMARY KEY AUTOINCREMENT, '
        f'name TEXT, color TEXT, balance TEXT, goal TEXT, currency TEXT)'
    )

    # transaction_db
    base.execute(
        f'CREATE TABLE IF NOT EXISTS transaction_db '
        f'(id INTEGER PRIMARY KEY AUTOINCREMENT, '
        f'date TEXT, type TEXT, from_id TEXT, to_id TEXT, '
        f'from_SUM TEXT, from_currency TEXT, '
        f'to_SUM TEXT, to_currency TEXT, note TEXT)'
    )

    base.execute('''
        CREATE TABLE IF NOT EXISTS budget_data_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            YYYYMM TEXT,
            budgeted REAL,
            currency TEXT,
            FOREIGN KEY(category_id) REFERENCES categories_db(id)
        )
    ''')

    base.execute('''
            CREATE TABLE IF NOT EXISTS budget_data_incomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                income_id INTEGER,
                YYYYMM TEXT,
                budgeted REAL,
                currency TEXT,
                FOREIGN KEY(income_id) REFERENCES incomes_db(id)
            )
        ''')

    base.execute('''
            CREATE TABLE IF NOT EXISTS budget_data_savings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                savings_id INTEGER,
                YYYYMM TEXT,
                budgeted REAL,
                currency TEXT,
                FOREIGN KEY(savings_id) REFERENCES savings_db(id)
            )
        ''')

    base.commit()


def accounts_db_read() -> dict:
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


def savings_db_read() -> dict:
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


def categories_db_read() -> dict:
    categories_data_dict = {}

    for row in cur.execute(f'SELECT * FROM categories_db').fetchall():
        category_id = 'categories_' + str(row[0])

        categories_data_dict[category_id] = {
            'Name': str(row[1]),
            'Color': json.loads(row[2]) if not row[2] is None else [0, 0, 0, 1],
            'Icon': str(row[3])
        }

    return categories_data_dict


def incomes_db_read() -> dict:
    incomes_data_dict = {}

    for row in cur.execute(f'SELECT * FROM incomes_db').fetchall():
        income_id = 'income_' + str(row[0])
        incomes_data_dict[income_id] = {
            'Name': row[1],
            'Color': json.loads(row[2]),
            'Icon': row[3]
        }

    return incomes_data_dict


def transaction_db_read() -> dict:
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
        transaction_dict[trans_id]['Comment'] = row[9]

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


"""
def budget_data_read for incomes:
    budget_data_read(id='Incomes_', db_name='budget_data_incomes')
"""


def budget_data_read(id='categories_', db_name='budget_data_categories') -> dict:
    budget_data_dict = {}

    for row in cur.execute(f'SELECT * FROM {db_name}').fetchall():
        year_month = row[2]
        categories_id = str(id) + str(row[1])

        if not year_month in budget_data_dict:
            budget_data_dict[year_month] = {}

        budget_data_dict[year_month][categories_id] = {}

        budget_data_dict[year_month][categories_id]['Budgeted'] = row[3]
        budget_data_dict[year_month][categories_id]['Currency'] = row[4]

    return budget_data_dict


def budget_data_write(db_name, data_dict) -> None:
    cur.execute(f"PRAGMA table_info({db_name})")
    columns = [row[1] for row in cur.fetchall()]

    cur.execute(f'INSERT INTO {db_name} '
                f"({', '.join(columns)}) "
                f'VALUES (NULL, ?, ?, ?, ?)',
                (data_dict['id'], data_dict['date'], data_dict['Budgeted'], data_dict['currency'])
                )
    base.commit()


def budget_data_cut(db_name, data_dict) -> None:
    cur.execute(f"PRAGMA table_info({db_name})")
    columns = [row[1] for row in cur.fetchall()]

    cur.execute(f"DELETE FROM {db_name} WHERE  {columns[1]} = ? AND  {columns[2]} = ? AND {columns[4]} = ? ",
                (data_dict['id'], data_dict['date'], data_dict['currency']))
    base.commit()


def budget_data_edit(db_name, data_dict) -> None:
    cur.execute(f"PRAGMA table_info({db_name})")
    columns = [row[1] for row in cur.fetchall()]

    cur.execute(f"SELECT * FROM {db_name} WHERE  {columns[1]} = ? AND  {columns[2]} = ? AND {columns[4]} = ?",
                (data_dict['id'], data_dict['date'], data_dict['currency']))
    row = cur.fetchone()
    if row:
        row_id = row[0]
        cur.execute(f"UPDATE {db_name} SET {columns[3]} = ? WHERE id = ?",
                    (data_dict['Budgeted'], row_id))
        base.commit()

    else:
        print("No matching row found")


def db_data_delete(db_name, item_id):
    if item_id is None:
        print(f"# There's nothing to delete: db_name={db_name}, item_id={item_id}")
        return

    type, id = item_id.split('_')

    cur.execute(f"DELETE FROM {db_name} WHERE id = ?", (id,))

    base.commit()

    print(f'# delete complete: db_name - {db_name}, id - {item_id}')

def db_data_edit(db_name: str, item_id: str, name: str = None, icon: str = None, color: list = None):
    query = f"UPDATE {db_name} SET "
    params = []

    if name is not None:
        query += "name = ?, "
        params.append(name)

    if icon is not None:
        query += "icon = ?, "
        params.append(icon)

    if color is not None:
        query += "color = ?, "
        params.append(json.dumps(color))

    if not params:
        print("# there is nothing to edit")
        return

    if item_id is None:
        print("# Edit doesn't complete: there's no item_id")
        return

    type, id = item_id.split('_')

    query = query[:-2]  # remove last ", "
    query += f" WHERE id = ?"
    params.append(id)

    cur.execute(query, params)

    print(f'# data updated: id={item_id}, params={params}')

    base.commit()

def db_data_add(db_name: str, params: dict):
    if not params['Color'] is list:
        params['Color'] = [0, 0, 0, 1]
        print('# Color is not a list, so now color=[0, 0, 0, 1]')

    params['Color'] = json.dumps(params['Color'])

    cur.execute(
        f'INSERT INTO {db_name} (name, color, icon) VALUES (?, ?, ?)',
        (params.get('Name'), params.get('Color'), params.get('Icon'))
    )
    base.commit()

    print(f"# Category created: Name={params.get('Name')}, Color={params.get('Color')}, Icon={params.get('Icon')}")
