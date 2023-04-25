from kivy.app import App
from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen

import config
from AppMenus.Transaction_menu.Transaction_menu_in import Transaction_menu_in
from AppMenus.other_func import load_previous_month, load_next_month, get_total_accounts_balance
from BasicMenus.CustomWidgets import TopNotification
from database import accounts_db_read, savings_db_read, categories_db_read, incomes_db_read


class Transaction_menu(MDScreen):
    total_accounts_balance = NumericProperty(get_total_accounts_balance())

    def __init__(self, *args, **kwargs):
        # getting actually data for menu settings and meny title
        self.current_menu_date = str(config.current_menu_date)[:-3]
        self.current_menu_month_name = config.current_menu_month_name
        self.days_in_month_icon_dict = config.days_in_month_icon_dict
        self.days_in_current_menu_month = config.days_in_current_menu_month

        super().__init__(*args, **kwargs)

    def update_total_accounts_balance(self, *args):
        self.ids.total_balance_label.text = str(get_total_accounts_balance())

    def load_previous_month(self):
        load_previous_month(self, Transaction_menu_in)

    def load_next_month(self):
        load_next_month(self, Transaction_menu_in)

    def open_menu_for_transaction_adding(self, *args):
        accounts_data = accounts_db_read() | savings_db_read()
        categories_data = categories_db_read() | incomes_db_read()

        if len(accounts_data) > 0 and len(categories_data) > 0:
            app = App.get_running_app()
            app.root.ids.main.open_menu_for_transaction_adding()

        else:
            TopNotification(text="Firstly create an account and an expense category").open()
