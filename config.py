import datetime
from calendar import monthrange, month_name

from kivymd.icon_definitions import md_icons

from AppData.data_scripts.GetData.GetHistoryDataForThePeriod import get_all_history_period

from database import categories_db_read, sql_start, accounts_db_read, savings_db_read, transaction_db_read

# app checking
start_app_time = datetime.datetime.now()

# ___date___
date_today = datetime.date.today()

current_year = date_today.year
current_month = date_today.month
current_day = date_today.day

# current menu date
days_in_month_icon_dict = {
    28: 'Icons/Month_days_icons/twenty-eight.png',
    29: 'Icons/Month_days_icons/twenty-nine.png',
    30: 'Icons/Month_days_icons/thirty.png',
    31: 'Icons/Month_days_icons/thirty-one.png'
}

current_menu_date = date_today

current_menu_year = current_year
current_menu_month = current_month

days_in_current_menu_month = monthrange(current_menu_year, current_menu_month)[1]
current_menu_month_name = month_name[current_menu_month]

# MainScreen
main_screen_pos = None
main_screen_size = None

sql_start()

# Accounts Menu
global_accounts_data_dict = accounts_db_read()

global_savings_data_dict = savings_db_read()

# Categories Menu
global_categories_data_dict = categories_db_read()

level = 0
color = None

icon_list = list(md_icons.keys())

# transaction menu
history_dict = transaction_db_read()

Transaction_menu_in_last_date = None

# all menus
months_loaded_at_startup = get_all_history_period(history_dict) + 1

if months_loaded_at_startup > 6:
    months_loaded_at_startup = 6

# menu for a new transaction
last_transaction_id = None
currency_symbol_dict = {
    'RUB': '₽',
    'USD': '$',
    'EUR': '€',
    None: None,
}
first_transaction_item = None
second_transaction_item = None
choosing_first_transaction = False
