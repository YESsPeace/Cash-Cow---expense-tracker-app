import os
import sys

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

import config

import AppMenus
from AppMenus import menu_for_a_new_transaction, Categories_buttons_menu, \
    Transaction_menu_in, BudgetMenu_in, menu_for_a_new_budget, menu_for_new_or_edit_category, \
    menu_for_choice_new_account_type, menu_for_new_account


class MainSrceen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        config.main_screen_pos = self.pos
        config.main_screen_size = self.size

    def open_menu_for_transaction_adding(self):
        self.ids.menu_for_transaction_adding.pos_hint = {'center_x': .5}
        self.ids.menu_for_transaction_adding.status = 'opened'

        self.ids.menu_for_transaction_adding.canvas.before.get_group('a')[0].pos = self.pos
        self.ids.menu_for_transaction_adding.canvas.before.get_group('a')[0].size = self.size

    def add_menu_for_a_new_transaction(self):
        self.add_widget(menu_for_a_new_transaction())

    def add_menu_for_a_new_budget(self):
        self.add_widget(menu_for_a_new_budget())

    def add_menu_for_new_or_edit_category(self):
        app = App.get_running_app()

        app.root.add_widget(
            menu_for_new_or_edit_category(
                name='menu_for_new_or_edit_category'
            ),
        )

        app.root.current = 'menu_for_new_or_edit_category'

    def add_menu_for_choice_account_type(self, new_account=True):
        self.add_widget(
            menu_for_choice_new_account_type(
                new_account=new_account
            )
        )

    def add_menu_for_new_account(self):
        app = App.get_running_app()

        app.root.add_widget(
            menu_for_new_account(
                id='menu_for_new_account',
                name='menu_for_new_account'
            ),
        )

        app.root.current = 'menu_for_new_account'

    def update_month_menu_group(self):
        month_screen_name = str(config.current_menu_date)[:-3]

        for month_menu in [(self.ids.CategoriesMenu, Categories_buttons_menu),
                           (self.ids.Transaction_menu, Transaction_menu_in),
                           (self.ids.BudgetMenu, BudgetMenu_in)]:

            if month_menu[0].ids.my_swiper.current != month_screen_name:
                month_menu[0].ids.month_label.text = config.current_menu_month_name
                month_menu[0].ids.month_icon.icon = config.days_in_month_icon_dict[
                    config.days_in_current_menu_month
                ]

                if month_menu[0].ids.my_swiper.has_screen(month_screen_name):
                    month_menu[0].ids.my_swiper.current = month_screen_name

                else:
                    month_menu[0].ids.my_swiper.add_widget(
                        month_menu[1](name=month_screen_name)
                    )


class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()


class MyNavigationDrawer(MDNavigationDrawer):

    def open_main(self):
        print(1)

    def open_other(self):
        print(2)


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class MoneyStatApp(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        self.theme_color = [0, 0, 0, 1]

        # loading multiple .kv files

        # Accounts menu
        Builder.load_file('AppMenus/Accounts_menu/accounts_menu.kv')
        Builder.load_file('AppMenus/Accounts_menu/accounts_menu_main.kv')
        Builder.load_file('AppMenus/Accounts_menu/accounts_menu_debts.kv')
        Builder.load_file('AppMenus/Accounts_menu/accounts_menu_stat.kv')

        # MenuForNewAccount
        Builder.load_file('AppMenus/Accounts_menu/MenuForNewAccount/menu_for_choice_new_account_type.kv')
        Builder.load_file('AppMenus/Accounts_menu/MenuForNewAccount/menu_for_new_account.kv')
        Builder.load_file('AppMenus/Accounts_menu/MenuForNewAccount/balance_writer.kv')

        # Categories menu
        Builder.load_file('AppMenus/Categories_menu/categories_menu.kv')
        Builder.load_file('AppMenus/Categories_menu/categories_buttons_menu.kv')
        Builder.load_file('AppMenus/Categories_menu/Incomes_buttons_menu.kv')

        Builder.load_file('AppMenus/Categories_menu/WaterFill.kv')

        # Menu_For_new_category
        Builder.load_file('AppMenus/CashMenus/MenuForAnewBudget.kv')
        Builder.load_file('AppMenus/Categories_menu/Menu_For_new_category/Menu_for_new_or_edit_category.kv')
        Builder.load_file('AppMenus/Categories_menu/Menu_For_new_category/icon_choice_menu.kv')

        # Transaction menu
        Builder.load_file('AppMenus/Transaction_menu/transaction_menu.kv')
        Builder.load_file('AppMenus/Transaction_menu/transaction_menu_in.kv')
        Builder.load_file('AppMenus/Transaction_menu/date_label_for_transaction_history_menu.kv')
        Builder.load_file('AppMenus/Transaction_menu/menu_for_transaction_adding.kv')

        # BudgeMenu
        Builder.load_file('AppMenus/Budget_menu/BudgetMenu.kv')
        Builder.load_file('AppMenus/Budget_menu/BudgetMenu_in.kv')

        # CashMenus
        Builder.load_file('AppMenus/CashMenus/menu_for_a_new_transaction.kv')

        # main
        Builder.load_file('main_screen.kv')
        Builder.load_file('my_navigation_drawer.kv')
        Builder.load_file('manager.kv')

        return Manager()


if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))

    # smartphone screen
    Window.size = (0.6 * 640, 0.6 * 1136)

    # start the app
    MoneyStatApp().run()
