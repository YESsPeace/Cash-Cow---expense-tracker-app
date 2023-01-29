import datetime
from calendar import monthrange, month_name

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

    def load_previous_month(self):
        last_month_date = config.current_menu_date - datetime.timedelta(days=config.days_in_current_menu_month)

        # update data in python
        config.current_menu_date = last_month_date

        config.days_in_current_menu_month = monthrange(config.current_menu_date.year, config.current_menu_date.month)[1]
        config.current_menu_month_name = month_name[config.current_menu_date.month]

        # update data in menu
        self.ids.month_label.text = config.current_menu_month_name
        self.ids.month_label.icon = config.days_in_month_icon_dict[config.days_in_current_menu_month]

        if self.ids.my_swiper.index == 0:
            self.ids.my_swiper.add_widget(Transaction_menu_in(name=last_month_date.strftime("%Y") + '-' +
                                                                   last_month_date.strftime("%m")), index=-1)
            print('After-previous', self.ids.my_swiper.slides)

        else:
            self.ids.my_swiper.index -= 1

    def load_next_month(self):
        # getting next month
        next_month_date = config.current_menu_date + datetime.timedelta(days=config.days_in_current_menu_month)

        # update data in python
        config.current_menu_date = next_month_date

        config.days_in_current_menu_month = monthrange(config.current_menu_date.year, config.current_menu_date.month)[1]
        config.current_menu_month_name = month_name[config.current_menu_date.month]

        # update data in menu
        self.ids.month_label.text = config.current_menu_month_name
        self.ids.month_label.icon = config.days_in_month_icon_dict[config.days_in_current_menu_month]

        if (self.ids.my_swiper.index == len(self.ids.my_swiper.slides) - 1) or \
                self.ids.my_swiper.next_slide.name != next_month_date.strftime("%Y") + \
                '-' + next_month_date.strftime("%m"):
            self.ids.my_swiper.add_widget(Transaction_menu_in(name=next_month_date.strftime("%Y") + '-' +
                                                                   next_month_date.strftime("%m")))
            # config.current_menu_month_name
            print('After-next', self.ids.my_swiper.slides)

        self.ids.my_swiper.index = self.ids.my_swiper.index + 1
