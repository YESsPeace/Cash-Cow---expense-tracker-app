import datetime
from calendar import monthrange, month_name

from kivy.uix.screenmanager import NoTransition
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock

import config
from AppData.data_scripts.GetData.GetHistoryDataForThePeriod import get_all_history_period
from AppMenus.Transaction_menu.Transaction_menu_in import Transaction_menu_in
from AppMenus.other_func import load_previous_month, load_next_month


class Transaction_menu(MDScreen):
    def __init__(self, *args, **kwargs):
        # getting history data
        print(*config.history_dict.items(), sep='\n')

        self.months_loaded_at_startup = config.months_loaded_at_startup

        print('months_loaded_at_startup:', self.months_loaded_at_startup)

        # getting actually data for menu settings and meny title
        self.current_menu_date = str(config.current_menu_date)[:-3]
        self.current_menu_month_name = config.current_menu_month_name
        self.days_in_month_icon_dict = config.days_in_month_icon_dict
        self.days_in_current_menu_month = config.days_in_current_menu_month

        super().__init__(*args, **kwargs)

        Clock.schedule_once(self.set_transition)
        Clock.schedule_once(self.add_pre_loaded_months)

    def set_transition(self, *args):
        self.ids.my_swiper.transition = NoTransition()

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