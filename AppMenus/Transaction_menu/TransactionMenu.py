from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

import config
from AppMenus.Transaction_menu.Transaction_menu_in import Transaction_menu_in
from AppMenus.other_func import load_previous_month, load_next_month, get_total_accounts_balance
from database import accounts_db_read, savings_db_read, categories_db_read, incomes_db_read


class Transaction_menu(MDScreen):
    total_accounts_balance = NumericProperty(get_total_accounts_balance())
    def __init__(self, *args, **kwargs):
        # getting history data
        self.months_loaded_at_startup = config.months_loaded_at_startup

        # getting actually data for menu settings and meny title
        self.current_menu_date = str(config.current_menu_date)[:-3]
        self.current_menu_month_name = config.current_menu_month_name
        self.days_in_month_icon_dict = config.days_in_month_icon_dict
        self.days_in_current_menu_month = config.days_in_current_menu_month

        super().__init__(*args, **kwargs)

        Clock.schedule_once(self.set_transition)
        # Clock.schedule_once(self.add_pre_loaded_months)

    def set_transition(self, *args):
        self.ids.my_swiper.transition = NoTransition()

    def update_total_accounts_balance(self, *args):
        self.ids.total_balance_label.text = str(get_total_accounts_balance())

    def add_pre_loaded_months(self, *args):
        print('TransactionMenu.add_pre_loaded_months')
        for _ in range(self.months_loaded_at_startup):
            self.load_previous_month()

        for _ in range(self.months_loaded_at_startup):
            self.load_next_month()

        print("TransactionMenu's Screens:", self.ids.my_swiper.screen_names)

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
            Snackbar(text="Firstly create an account and an expense category").open()