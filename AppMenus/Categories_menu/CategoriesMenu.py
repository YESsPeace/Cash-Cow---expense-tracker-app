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
        for swiper_id, menu_id in [('my_swiper', 'GridCategoriesMenu'), ('incomes_swiper', 'GridIncomesMenu')]:
            for box in getattr(getattr(self.ids, swiper_id).get_screen(self.current_menu_date).ids, menu_id).children:
                for container in box.children:
                    for button in container.children:
                        try:
                            button.unbind(on_release=getattr(self.ids, swiper_id).get_screen(
                                self.current_menu_date).open_menu_for_a_new_transaction)

                            button.bind(on_release=self.open_menu_for_edit_categories)

                        except AttributeError:
                            continue

            getattr(self.ids, swiper_id).get_screen(self.current_menu_date).add_plus_button()

    def quit_from_edit_mode(self, *args):
        print('# quit from edit mode')
        self.ids.top_bar.height = dp(100)

        self.ids.top_bar.clear_widgets()

        self.ids.top_bar.add_widget(self.top_btn_bar)
        self.ids.top_bar.add_widget(self.month_menu)

        for swiper_id in ['my_swiper', 'incomes_swiper']:
            getattr(self.ids, swiper_id).get_screen(self.current_menu_date).del_plus_button()

        # rebind buttons functions
        for swiper_id, menu_id, plus_button_id in \
                [('my_swiper', 'GridCategoriesMenu', 'plus_button_categories'),
                 ('incomes_swiper', 'GridIncomesMenu', 'plus_button_incomes')]:
            for box in getattr(getattr(self.ids, swiper_id).get_screen(self.current_menu_date).ids, menu_id).children:
                for container in box.children:
                    for button in container.children:
                        try:
                            print(button.id)

                            if button.id == plus_button_id:
                                continue

                            button.unbind(on_release=self.open_menu_for_edit_categories)

                            button.bind(on_release= \
                                            getattr(self.ids, swiper_id).get_screen(
                                                self.current_menu_date).open_menu_for_a_new_transaction)

                        except AttributeError:
                            continue

    def open_menu_for_edit_categories(self, button, *args):
        print(f'# Clicked - {button.id}')

        self.quit_from_edit_mode()

        if button.id in ['plus_button_categories', 'plus_button_incomes']:
            config.category_item = {
                'ID': None,
                'Name': '',
                'Color': [0.71, 0.72, 0.69, 0.5],
                'Icon': 'basket-outline',
                'new': True,
                'db_name': button.id.split('_')[-1] + '_db'
            }

        else:
            config.category_item = (categories_db_read() | incomes_db_read()).get(button.id)
            config.category_item['ID'] = button.id
            config.category_item['db_name'] = 'categories_db' \
                if button.id.split('_')[0] == 'categories' else 'incomes_db'

        app = App.get_running_app()

        app.root.ids.main.add_menu_for_new_or_edit_category()
