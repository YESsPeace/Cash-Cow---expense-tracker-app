from kivy.app import App
from kivy.lang import Builder
from kivy.properties import Clock, StringProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.screen import MDScreen

import config
from BasicMenus import TopNotification, BoxLayoutButton
from database import sql_start

sql_start()

from AppMenus import *


class MainSrceen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        config.main_screen_pos = self.pos
        config.main_screen_size = self.size

    def open_menu_for_transaction_adding(
            self,
            choosing_first_transaction=False,
            choosing_second_transaction=True,
            first_transaction_item=None,
            second_transaction_item=None,
    ):
        if not first_transaction_item is None:
            self.add_widget(
                MenuForTransactionAdding(
                    choosing_first_transaction=choosing_first_transaction,
                    choosing_second_transaction=choosing_second_transaction,
                    first_transaction_item=first_transaction_item,
                )
            )

        elif not second_transaction_item is None:
            self.add_widget(
                MenuForTransactionAdding(
                    choosing_first_transaction=choosing_first_transaction,
                    choosing_second_transaction=choosing_second_transaction,
                    second_transaction_item=second_transaction_item
                )
            )

        else:
            self.add_widget(
                MenuForTransactionAdding(
                    choosing_first_transaction=choosing_first_transaction,
                    choosing_second_transaction=choosing_second_transaction,
                )
            )

    def open_menu_for_transaction_info(self, transaction_id, transaction_data, *args):
        self.add_widget(
            menu_for_transaction_info(
                transaction_id=transaction_id,
                transaction_data=transaction_data
            )
        )

    def add_menu_for_a_new_transaction(
            self,
            transaction_id=0,
            transaction_data=None,
            edit_transaction_mode=False,
            first_transaction_item=None,
            second_transaction_item=None,
    ):
        if (not first_transaction_item is None) and (not second_transaction_item is None):
            if not transaction_data is None:
                self.add_widget(
                    menu_for_a_new_transaction(
                        transaction_id=transaction_id,
                        transaction_data=transaction_data,
                        edit_transaction_mode=edit_transaction_mode,
                        first_transaction_item=first_transaction_item,
                        second_transaction_item=second_transaction_item
                    )
                )

            else:
                self.add_widget(
                    menu_for_a_new_transaction(
                        transaction_id=transaction_id,
                        edit_transaction_mode=edit_transaction_mode,
                        first_transaction_item=first_transaction_item,
                        second_transaction_item=second_transaction_item
                    )
                )


        else:
            TopNotification(text="There's no first or second transaction item").open()

    def add_menu_for_edit_budget(self, widget_id):
        self.add_widget(menu_for_edit_budget(widget_id=widget_id))

    def add_menu_for_choice_a_budget_item(self):
        self.add_widget(MenuForChoiceABudgetItem())

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

        app.root.ids.main_screen_manager.add_widget(
            menu_for_new_account(
                id='menu_for_new_account',
                name='menu_for_new_account'
            ),
        )

        app.root.ids.main_screen_manager.current = 'menu_for_new_account'

    def update_month_menu_group(self):
        month_screen_name = str(config.current_menu_date)[:-3]

        for month_menu in [(self.ids.CategoriesMenu, Categories_buttons_menu),
                           (self.ids.CategoriesMenu, Incomes_buttons_menu),
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

                    month_menu[0].ids.my_swiper.current = month_screen_name

                if config.current_menu_date.strftime("%Y") + config.current_menu_date.strftime("%m") == \
                        config.date_today.strftime("%Y") + config.date_today.strftime("%m"):
                    month_menu[0].ids.top_bar.md_bg_color = [.6, .1, .2, 1]


                else:
                    month_menu[0].ids.top_bar.md_bg_color = [.33, .33, .33, 1]


class My_BottomNavigation(MDBottomNavigation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.set_widget_props, -1)

    def set_widget_props(self, *args):
        Clock.schedule_once(self.set_transition, -1)

    def set_transition(self, *args):
        self.ids.tab_manager.transition = SlideTransition(duration=.75)


class Manager(MDScreen):
    pass


class MyNavigationDrawer(MDNavigationDrawer):
    pass


class DrawerClickableItem(BoxLayoutButton):
    button_name = StringProperty('')


class MoneyStatApp(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        self.theme_color = [.1, .1, .1, 1]

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

        # Menu_For_new_category
        Builder.load_file('AppMenus/Categories_menu/Menu_For_new_category/Menu_for_new_or_edit_category.kv')
        Builder.load_file('AppMenus/Categories_menu/Menu_For_new_category/icon_choice_menu.kv')

        # Transaction menu
        Builder.load_file('AppMenus/Transaction_menu/transaction_menu.kv')
        Builder.load_file('AppMenus/Transaction_menu/transaction_menu_in.kv')
        Builder.load_file('AppMenus/Transaction_menu/menu_for_transaction_adding.kv')
        Builder.load_file('AppMenus/Transaction_menu/menu_for_transaction_info.kv')

        # BudgeMenu
        Builder.load_file('AppMenus/Budget_menu/BudgetMenu.kv')
        Builder.load_file('AppMenus/Budget_menu/BudgetMenu_in.kv')
        Builder.load_file('AppMenus/Budget_menu/MenuForChoiceABudgetItem.kv')

        # CashMenus
        Builder.load_file('AppMenus/CashMenus/menu_for_a_new_transaction.kv')
        Builder.load_file('AppMenus/CashMenus/MenuForEditBudget.kv')

        # BasicMenus
        Builder.load_file('BasicMenus/CustomWidgets.kv')

        # SettingsMenu
        Builder.load_file('AppMenus/SettingsMenus/ExportMenu.kv')

        # main
        Builder.load_file('main_screen.kv')
        Builder.load_file('my_navigation_drawer.kv')
        Builder.load_file('manager.kv')

        return Manager()


if __name__ == '__main__':
    # start the app
    MoneyStatApp().run()
