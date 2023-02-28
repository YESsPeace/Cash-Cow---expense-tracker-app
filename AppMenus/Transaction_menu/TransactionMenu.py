import datetime
from calendar import monthrange, month_name
from time import sleep

from kivy.uix.screenmanager import NoTransition
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock

import config
from AppData.data_scripts.GetData.GetHistoryDataForThePeriod import get_transaction_history
from AppMenus.Transaction_menu.Transaction_menu_in import Transaction_menu_in


class Transaction_menu(MDScreen):
    # getting history data
    config.history_dict = get_transaction_history(
        history_file_path='AppData/data_files/transaction-history.csv',
    )
    print(*config.history_dict.items(), sep='\n')

    def __init__(self, *args, **kwargs):
        # getting history data
        config.history_dict = get_transaction_history(
            history_file_path='AppData/data_files/transaction-history.csv',
        )
        print(*config.history_dict.items(), sep='\n')

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
        for _ in range(config.months_loaded_at_startup):
            self.load_previous_month()

        for _ in range(config.months_loaded_at_startup * 2):
            self.load_next_month()

        for _ in range(config.months_loaded_at_startup):
            self.load_previous_month()

        print('TransactionMenu', self.ids.my_swiper.screen_names)

    def load_previous_month(self):

        config.current_menu_date = config.current_menu_date.replace(day=1)

        last_month_date = config.current_menu_date - datetime.timedelta(days=1)

        # update data in python
        config.current_menu_date = last_month_date

        config.days_in_current_menu_month = monthrange(config.current_menu_date.year, config.current_menu_date.month)[1]
        config.current_menu_month_name = month_name[config.current_menu_date.month]

        # update data in menu
        self.ids.month_label.text = config.current_menu_month_name
        self.ids.month_icon.icon = config.days_in_month_icon_dict[config.days_in_current_menu_month]

        name_ = last_month_date.strftime("%Y") + '-' + last_month_date.strftime("%m")

        if not self.ids.my_swiper.has_screen(name_):
            self.ids.my_swiper.add_widget(Transaction_menu_in(name=name_))

        self.ids.my_swiper.current = name_

        print('now screen name is', name_)

    def load_next_month(self):

        config.current_menu_date = config.current_menu_date.replace(day=int(config.days_in_current_menu_month))

        # getting next month
        next_month_date = config.current_menu_date + datetime.timedelta(days=1)

        # update data in python
        config.current_menu_date = next_month_date

        config.days_in_current_menu_month = monthrange(config.current_menu_date.year, config.current_menu_date.month)[1]
        config.current_menu_month_name = month_name[config.current_menu_date.month]

        # update data in menu
        self.ids.month_label.text = config.current_menu_month_name
        self.ids.month_icon.icon = config.days_in_month_icon_dict[config.days_in_current_menu_month]

        name_ = next_month_date.strftime("%Y") + '-' + next_month_date.strftime("%m")

        if not self.ids.my_swiper.has_screen(name_):
            self.ids.my_swiper.add_widget(Transaction_menu_in(name=name_))

        self.ids.my_swiper.current = name_
