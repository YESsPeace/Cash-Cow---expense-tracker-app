import datetime
from calendar import monthrange, month_name

from kivymd.icon_definitions import md_icons

from AppData.data_scripts.GetData.GetDataFilesData import get_accounts_data, get_savings_data, get_categories_data_from
from AppData.data_scripts.GetData.GetHistoryDataForThePeriod import get_all_history_period, get_transaction_history

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


# Accounts Menu
global_accounts_data_dict = get_accounts_data(
        accounts_data_file_path='AppData/data_files/accounts-data.txt'
    )
global_savings_data_dict = get_savings_data(
        savings_data_file_path='AppData/data_files/savings-data.txt'
    )

# Categories Menu
global_categories_data_dict = get_categories_data_from(
        categories_data_file_path='AppData/data_files/categories-data.txt'
    )
level = 0
color = None

icon_list = list(md_icons.keys())

# transaction menu
history_dict = get_transaction_history(
            history_file_path='AppData/data_files/transaction-history.csv',
        )
Transaction_menu_in_last_date = None

# all menus
months_loaded_at_startup = get_all_history_period(history_dict) + 1

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
