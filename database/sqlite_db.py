import json
import sqlite3 as sq


def sql_start() -> None:
    base = sq.connect('AppDataBase.db')
    if base:
        print('# [Database] connected and created OK')

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
        f'name TEXT, color TEXT, balance REAL, currency TEXT, IncludeInTheTotalBalance INTEGER, '
        f'Description TEXT, icon TEXT)'
    )

    # savings_db
    base.execute(
        f'CREATE TABLE IF NOT EXISTS savings_db '
        f'(id INTEGER PRIMARY KEY AUTOINCREMENT, '
        f'name TEXT, color TEXT, balance REAL, goal REAL, currency TEXT, IncludeInTheTotalBalance INTEGER, '
        f'Description TEXT, icon TEXT)'
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
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

    accounts_data_dict = {}

    for row in cur.execute(f'SELECT * FROM accounts_db').fetchall():
        account_id = 'account_' + str(row[0])

        accounts_data_dict[account_id] = {
            'Name': row[1],
            'Color': json.loads(row[2]),
            'Balance': float(row[3]),
            'Currency': row[4],
            'IncludeInTheTotalBalance': row[5],
            'Description': row[6],
            'Icon': row[7]
        }

    return accounts_data_dict


def savings_db_read() -> dict:
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

    savings_data_dict = {}

    for row in cur.execute(f'SELECT * FROM savings_db').fetchall():
        savings_id = 'savings_' + str(row[0])

        savings_data_dict[savings_id] = {
            'Name': row[1],
            'Color': json.loads(row[2]),
            'Balance': row[3],
            'Goal': row[4],
            'Currency': row[5],
            'IncludeInTheTotalBalance': row[6],
            'Description': row[7],
            'Icon': row[8]
        }

    return savings_data_dict


def categories_db_read() -> dict:
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

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
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

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
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

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
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

    cur.execute(f'INSERT INTO transaction_db '
                f'(date, type, from_id, to_id, from_SUM, from_currency, to_SUM, to_currency, note) '
                f'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (trans_data_dict['Date'], trans_data_dict['Type'], trans_data_dict['From'], trans_data_dict['To'],
                 str(trans_data_dict['FromSUM']), trans_data_dict['FromCurrency'], str(trans_data_dict['ToSUM']),
                 trans_data_dict['ToCurrency'], trans_data_dict['Comment'])
                )
    base.commit()
    print('# transaction written:', *trans_data_dict.items(), sep='\n')

    for account in {trans_data_dict['From']: -trans_data_dict['FromSUM'],
                    trans_data_dict['To']: trans_data_dict['ToSUM']}.items():
        accounts_and_savings_db_edit_balance(
            db_name='savings_db' if account[0].split('_')[0] == 'savings' else 'accounts_db',
            item_id=account[0],
            balance_difference=account[1]

        )


def get_transaction_data_by_id(transaction_id: int) -> dict:
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

    cur.execute("SELECT * FROM transaction_db WHERE id = ?", (transaction_id,))
    transaction = cur.fetchone()

    if transaction:
        id, date, type, from_id, to_id, from_SUM, from_currency, to_SUM, to_currency, note = transaction
        return dict(id=id, Date=date, Type=type,
                    From=from_id, To=to_id,
                    FromSUM=float(from_SUM), FromCurrency=from_currency,
                    ToSUM=float(to_SUM), ToCurrency=to_currency, Comment=note)


    else:
        print("# transaction not found")


def delete_transaction(transaction_id: int) -> None:
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

    if not type(transaction_id) is int:
        print('# transaction_id is not int')
        return

    transaction_data = get_transaction_data_by_id(transaction_id)

    if not transaction_data is None:
        cur.execute("DELETE FROM transaction_db WHERE id = ?", (transaction_id,))

        base.commit()

        for account in {transaction_data['From']: transaction_data['FromSUM'],
                        transaction_data['To']: -transaction_data['ToSUM']}.items():
            accounts_and_savings_db_edit_balance(
                db_name='savings_db' if account[0].split('_')[0] == 'savings' else 'accounts_db',
                item_id=account[0],
                balance_difference=account[1]
            )


def edit_transaction(transaction_id: int, transaction_data: dict) -> None:
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

    if not type(transaction_id) is int:
        print("# transaction_id is not int it's", type(transaction_id))
        return

    if not type(transaction_id) is int:
        print("# transaction_data is not dict it's", type(transaction_data))
        return

    old_transaction_data = get_transaction_data_by_id(transaction_id)

    cur.execute(
        f"UPDATE transaction_db SET "
        f"{'date = ?, type = ?, from_id = ?, to_id = ?, from_SUM = ?, from_currency = ?, to_SUM = ?, to_currency = ?, note = ?'} WHERE id = ?",
        (transaction_data['Date'], transaction_data['Type'], transaction_data['From'], transaction_data['To'],
         transaction_data['FromSUM'], transaction_data['FromCurrency'], transaction_data['ToSUM'],
         transaction_data['ToCurrency'],
         transaction_data['Comment'],
         transaction_id))

    base.commit()

    for account in {old_transaction_data['From']: (old_transaction_data['FromSUM'] - transaction_data['FromSUM']),
                    old_transaction_data['To']: -(old_transaction_data['ToSUM'] - transaction_data['FromSUM'])}.items():
        accounts_and_savings_db_edit_balance(
            db_name='savings_db' if account[0].split('_')[0] == 'savings' else 'accounts_db',
            item_id=account[0],
            balance_difference=account[1]
        )

    base.commit()


"""
def budget_data_read for incomes:
    budget_data_read(id='Incomes_', db_name='budget_data_incomes')
"""


def budget_data_read(id='categories_', db_name='budget_data_categories') -> dict:
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

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
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

    cur.execute(f"PRAGMA table_info({db_name})")
    columns = [row[1] for row in cur.fetchall()]

    cur.execute(f'INSERT INTO {db_name} '
                f"({', '.join(columns)}) "
                f'VALUES (NULL, ?, ?, ?, ?)',
                (data_dict['id'], data_dict['date'], data_dict['Budgeted'], data_dict['currency'])
                )
    base.commit()


def budget_data_cut(db_name, data_dict) -> None:
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

    cur.execute(f"PRAGMA table_info({db_name})")
    columns = [row[1] for row in cur.fetchall()]

    cur.execute(f"DELETE FROM {db_name} WHERE  {columns[1]} = ? AND  {columns[2]} = ? AND {columns[4]} = ? ",
                (data_dict['id'], data_dict['date'], data_dict['currency']))
    base.commit()


def budget_data_edit(db_name, data_dict) -> None:
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

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
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

    if item_id is None:
        print(f"# There's nothing to delete: db_name={db_name}, item_id={item_id}")
        return

    type, id = item_id.split('_')

    cur.execute(f"DELETE FROM {db_name} WHERE id = ?", (id,))

    base.commit()

    print(f'# delete complete: db_name - {db_name}, id - {item_id}')


def db_data_edit(db_name: str, item_id: str, name: str = None, icon: str = None, color: list = None):
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

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
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

    if params.get('Color') is None:
        params['Color'] = [0, 0, 0, 1]
        print('# Color is not a list, so now color=[0, 0, 0, 1]')

    params['Color'] = json.dumps(params['Color'])

    cur.execute(
        f'INSERT INTO {db_name} (name, color, icon) VALUES (?, ?, ?)',
        (params.get('Name'), params.get('Color'), params.get('Icon'))
    )
    base.commit()

    print(f"# Category created: Name={params.get('Name')}, Color={params.get('Color')}, Icon={params.get('Icon')}")


def account_db_add(params: dict):
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

    cur.execute(f"PRAGMA table_info(accounts_db)")
    columns = [row[1] for row in cur.fetchall()]

    if params.get('Color') is None:
        params['Color'] = [0, 0, 0, 1]
        print('# Color is not a list, so now color=[0, 0, 0, 1]')

    params['Color'] = json.dumps(params['Color'])

    cur.execute(f'INSERT INTO accounts_db '
                f"({', '.join(columns)}) "
                f"VALUES (NULL, {', '.join(['?' for _ in range(len(columns) - 1)])})",
                (params.get('Name'), params.get('Color'),
                 params.get('Balance'), params.get('Currency'),
                 params.get('IncludeInTheTotalBalance'),
                 params.get('Description'), params.get('Icon'))
                )
    base.commit()


def savings_db_add(params: dict):
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

    cur.execute(f"PRAGMA table_info(savings_db)")
    columns = [row[1] for row in cur.fetchall()]

    if params.get('Color') is None:
        params['Color'] = [0, 0, 0, 1]
        print('# Color is not a list, so now color=[0, 0, 0, 1]')

    params['Color'] = json.dumps(params['Color'])

    cur.execute(f'INSERT INTO savings_db '
                f"({', '.join(columns)}) "
                f"VALUES (NULL, {', '.join(['?' for _ in range(len(columns) - 1)])})",
                (params.get('Name'), params.get('Color'),
                 params.get('Balance'), params.get('Goal'),
                 params.get('Currency'),
                 params.get('IncludeInTheTotalBalance'),
                 params.get('Description'), params.get('Icon'))
                )
    base.commit()


def accounts_db_edit(params: dict):
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

    if params.get('Color') is None:
        params['Color'] = [0, 0, 0, 1]
        print('# Color is not a list, so now color=[0, 0, 0, 1]')

    params['Color'] = json.dumps(params['Color'])

    type, id = params['ID'].split('_')

    cur.execute(f"UPDATE accounts_db SET "
                f"name=?, color=?, balance=?, currency=?, IncludeInTheTotalBalance=?, Description=?, icon=? "
                f"WHERE id=?",
                (params.get('Name'), params.get('Color'),
                 params.get('Balance'), params.get('Currency'),
                 params.get('IncludeInTheTotalBalance'),
                 params.get('Description'), params.get('Icon'),
                 id)
                )
    base.commit()

    print(f'# {params["ID"]} edited: ', *params.items(), sep='\n')


def savings_db_edit(params: dict):
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

    if params.get('Color') is None:
        params['Color'] = [0, 0, 0, 1]
        print('# Color is not a list, so now color=[0, 0, 0, 1]')

    params['Color'] = json.dumps(params['Color'])

    type, id = params['ID'].split('_')

    cur.execute(f"UPDATE savings_db SET "
                f"name=?, color=?, balance=?, goal=?, currency=?, IncludeInTheTotalBalance=?, Description=?, icon=? "
                f"WHERE id=?",
                (params.get('Name'), params.get('Color'),
                 params.get('Balance'), params.get('Goal'),
                 params.get('Currency'),
                 params.get('IncludeInTheTotalBalance'),
                 params.get('Description'), params.get('Icon'),
                 id)
                )
    base.commit()

    print(f'# {params["ID"]} edited: ', *params.items(), sep='\n')


def accounts_and_savings_db_edit_balance(db_name: str, item_id: str, balance_difference: int = 0):
    base = sq.connect('AppDataBase.db')
    cur = base.cursor()

    type, id = item_id.split('_')

    db_data = accounts_db_read() | savings_db_read()

    if item_id not in db_data:
        print(f'# {item_id} is not found in {db_name}')
        return

    balance = db_data[item_id]['Balance']
    balance += balance_difference

    cur.execute(f"UPDATE {db_name} SET "
                f"balance=? "
                f"WHERE id=?",
                (balance, id)
                )
    base.commit()

    print(f'# {item_id} balance updated:', balance)
