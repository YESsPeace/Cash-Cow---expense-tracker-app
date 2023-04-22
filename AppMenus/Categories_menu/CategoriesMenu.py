from copy import copy

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

import config
from AppMenus.Categories_menu.Incomes_buttons_menu import Incomes_buttons_menu

from AppMenus.other_func import load_next_month, load_previous_month, get_total_accounts_balance

from AppMenus.Categories_menu.Categories_buttons_menu import Categories_buttons_menu
from database import categories_db_read, incomes_db_read


class CategoriesMenu(MDScreen):
    total_accounts_balance = NumericProperty(get_total_accounts_balance())

    def __init__(self, *args, **kwargs):

        # just for first creating widgets
        self.current_menu_date = str(config.current_menu_date)[:-3]
        self.current_menu_month_name = config.current_menu_month_name
        self.days_in_month_icon_dict = config.days_in_month_icon_dict
        self.days_in_current_menu_month = config.days_in_current_menu_month

        super().__init__(*args, **kwargs)

        self.months_loaded_at_startup = config.months_loaded_at_startup

        Clock.schedule_once(self.set_transition)
        # Clock.schedule_once(self.add_pre_loaded_months)

    def update_total_accounts_balance(self, *args):
        self.ids.total_balance_label.text = str(get_total_accounts_balance())

    def set_transition(self, *args):
        self.ids.my_swiper.transition = NoTransition()
        self.ids.incomes_swiper.transition = NoTransition()

    def add_pre_loaded_months(self, *args):
        print('CategoriesMenu.add_pre_loaded_months')
        for _ in range(self.months_loaded_at_startup):
            self.load_previous_month()

        for _ in range(self.months_loaded_at_startup):
            self.load_next_month()

        print("CategoriesMenu's Screens", self.ids.my_swiper.screen_names)

    def load_previous_month(self):
        load_previous_month(self, Categories_buttons_menu)

        name_ = str(config.current_menu_date)[:-3]

        if not self.ids.incomes_swiper.has_screen(name_):
            self.ids.incomes_swiper.add_widget(Incomes_buttons_menu(name=name_))

        self.ids.incomes_swiper.current = name_

    def load_next_month(self):
        load_next_month(self, Categories_buttons_menu)

        name_ = str(config.current_menu_date)[:-3]

        if not self.ids.incomes_swiper.has_screen(name_):
            self.ids.incomes_swiper.add_widget(Incomes_buttons_menu(name=name_))

        self.ids.incomes_swiper.current = name_

    def start_edit_mode(self, *args):
        print('# start edit mode')

        # switch top_bar to edit mode
        self.top_btn_bar = copy(self.ids.top_btn_bar)
        self.month_menu = copy(self.ids.month_menu)

        self.ids.top_bar.clear_widgets()
        self.ids.top_bar.height = dp(48)

        edit_mode_top_bar = \
            MDBoxLayout(
                MDBoxLayout(
                    MDIconButton(
                        icon='arrow-left',
                        on_release=self.quit_from_edit_mode
                    ),
                    MDLabel(
                        text='Редактирование',
                        halign='left',
                    ),
                    orientation='horizontal',
                    md_bg_color=(.2, .4, .85, 1),
                ),
                orientation='vertical',
            )

        self.ids.top_bar.add_widget(
            edit_mode_top_bar
        )

        # rebind buttons functions
        for swiper_id, rv_id in [('my_swiper', 'Categories_rv'), ('incomes_swiper', 'Incomes_rv')]:
            new_data = getattr(self.ids, swiper_id).get_screen(self.current_menu_date).get_rv_data()

            for item in new_data:
                item['on_release'] = self.on_category_callback(item['category_id'])

            new_data.append(
                {
                    "viewclass": "CategoryItem",
                    "height": dp(80),
                    "category_data": {
                        'Name': 'Добавить',
                        'Color': [.33, .33, .33, 1],
                        'Icon': 'plus',
                    },
                    "on_release": self.on_category_callback('plus_button_categories')
                }
            )

            getattr(getattr(self.ids, swiper_id).get_screen(self.current_menu_date).ids, rv_id).data = new_data

    def on_category_callback(self, category_id):
        return lambda: self.open_menu_for_edit_categories(category_id)

    def quit_from_edit_mode(self, *args):
        print('# quit from edit mode')
        self.ids.top_bar.height = dp(100)

        self.ids.top_bar.clear_widgets()

        self.ids.top_bar.add_widget(self.top_btn_bar)
        self.ids.top_bar.add_widget(self.month_menu)

        # rebind buttons functions
        for swiper_id, rv_id in [('my_swiper', 'Categories_rv'), ('incomes_swiper', 'Incomes_rv')]:
            getattr(self.ids, swiper_id).get_screen(self.current_menu_date).refresh_rv_data()

    def open_menu_for_edit_categories(self, category_id, *args):
        print(f'# Clicked - {category_id}')

        self.quit_from_edit_mode()

        if category_id in ['plus_button_categories', 'plus_button_incomes']:
            config.category_item = {
                'ID': None,
                'Name': '',
                'Color': [0.71, 0.72, 0.69, 0.5],
                'Icon': 'basket-outline',
                'new': True,
                'db_name': category_id.split('_')[-1] + '_db'
            }

        else:
            config.category_item = (categories_db_read() | incomes_db_read()).get(category_id)
            config.category_item['ID'] = category_id
            config.category_item['db_name'] = 'categories_db' \
                if category_id.split('_')[0] == 'categories' else 'incomes_db'

        app = App.get_running_app()

        app.root.ids.main.add_menu_for_new_or_edit_category()
