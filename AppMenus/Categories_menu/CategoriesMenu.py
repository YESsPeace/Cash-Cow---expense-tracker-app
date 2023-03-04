from kivy.clock import Clock
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.screen import MDScreen

import config

from AppMenus.other_func import load_next_month, load_previous_month

from AppMenus.Categories_menu.Categories_buttons_menu import Categories_buttons_menu


class CategoriesMenu(MDScreen):
    def __init__(self, *args, **kwargs):

        # just for first creating widgets
        self.current_menu_date = str(config.current_menu_date)[:-3]
        self.current_menu_month_name = config.current_menu_month_name
        self.days_in_month_icon_dict = config.days_in_month_icon_dict
        self.days_in_current_menu_month = config.days_in_current_menu_month

        super().__init__(*args, **kwargs)

        self.months_loaded_at_startup = config.months_loaded_at_startup

        Clock.schedule_once(self.set_transition)
        Clock.schedule_once(self.add_pre_loaded_months)

    def set_transition(self, *args):
        self.ids.my_swiper.transition = NoTransition()

    def add_pre_loaded_months(self, *args):
        print('CategoriesMenu.add_pre_loaded_months')
        for _ in range(self.months_loaded_at_startup):
            self.load_previous_month()

        for _ in range(self.months_loaded_at_startup):
            self.load_next_month()


        print("CategoriesMenu's Screens", self.ids.my_swiper.screen_names)

    def load_previous_month(self):
        load_previous_month(self, Categories_buttons_menu)

    def load_next_month(self):
        load_next_month(self, Categories_buttons_menu)
