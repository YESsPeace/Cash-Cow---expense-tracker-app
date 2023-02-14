import datetime
from calendar import month_name, monthrange

from kivy.clock import Clock
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.screen import MDScreen

import config
from AppData.data_scripts.GetData.GetDataFilesData import get_categories_data_from
from AppMenus.Categories_menu.Categories_buttons_menu import Categories_buttons_menu


class CategoriesMenu(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # getting data for categories
        config.global_categories_data_dict = get_categories_data_from(
            categories_data_file_path='AppData/data_files/categories-data.txt'
        )

        # just for first creating widgets
        self.current_menu_date = str(config.current_menu_date)[:-3]
        self.current_menu_month_name = config.current_menu_month_name
        self.days_in_month_icon_dict = config.days_in_month_icon_dict
        self.days_in_current_menu_month = config.days_in_current_menu_month

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

        print('CategoriesMenu', self.ids.my_swiper.screen_names)

    def load_previous_month(self):
        last_month_date = config.current_menu_date - datetime.timedelta(days=config.days_in_current_menu_month)

        # update data in python
        config.current_menu_date = last_month_date

        config.days_in_current_menu_month = monthrange(config.current_menu_date.year, config.current_menu_date.month)[1]
        config.current_menu_month_name = month_name[config.current_menu_date.month]

        # update data in menu
        self.ids.month_label.text = config.current_menu_month_name
        self.ids.month_icon.icon = config.days_in_month_icon_dict[config.days_in_current_menu_month]

        name_ = last_month_date.strftime("%Y") + '-' + last_month_date.strftime("%m")

        if not self.ids.my_swiper.has_screen(name_):
            self.ids.my_swiper.add_widget(Categories_buttons_menu(name=name_))

        self.ids.my_swiper.current = name_

    def load_next_month(self):
        # getting next month
        next_month_date = config.current_menu_date + datetime.timedelta(days=config.days_in_current_menu_month)

        # update data in python
        config.current_menu_date = next_month_date

        config.days_in_current_menu_month = monthrange(config.current_menu_date.year, config.current_menu_date.month)[1]
        config.current_menu_month_name = month_name[config.current_menu_date.month]

        # update data in menu
        self.ids.month_label.text = config.current_menu_month_name
        self.ids.month_icon.icon = config.days_in_month_icon_dict[config.days_in_current_menu_month]

        name_ = next_month_date.strftime("%Y") + '-' + next_month_date.strftime("%m")

        if not self.ids.my_swiper.has_screen(name_):
            self.ids.my_swiper.add_widget(Categories_buttons_menu(name=name_))

        self.ids.my_swiper.current = name_