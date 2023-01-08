from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, BooleanProperty, OptionProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

from AppMenus.Accounts_menu.AccountsMenu import AccountsMenu
from AppMenus.Accounts_menu.AccountsMenu_main import AccountsMenu_main
from AppMenus.Accounts_menu.AccountsMenu_debts import AccountsMenu_debts
from AppMenus.Accounts_menu.AccountsMenu_stat import AccountsMenu_stat

from AppMenus.Categories_menu.CategoriesMenu import CategoriesMenu
from AppMenus.Categories_menu.Categories_buttons_menu import Categories_buttons_menu

from AppMenus.Transaction_menu.TransactionMenu import Transaction_menu
from AppMenus.Transaction_menu.Transaction_menu_in import Transaction_menu_in
from AppMenus.Transaction_menu.date_label_for_transaction_history_menu import date_label_for_transaction_history_menu

import config

from AppData.data_scripts.Creating_data_files.CsvTransactionHistory import create_transaction_history_file
from AppData.data_scripts.Creating_data_files.TxtAccountsData import create_accounts_data_file
from AppData.data_scripts.Creating_data_files.TxtCategoriesData import create_categories_data_file
from AppData.data_scripts.Creating_data_files.TxtSavingsData import create_savings_data_file
from AppData.data_scripts.GetData.GetDataFilesData import get_accounts_data, get_categories_data_from, get_savings_data


class MainSrceen(MDScreen):
    def open_menu_for_transaction_adding(self):
        self.ids.menu_for_transaction_adding.pos_hint = {'center_x': .5}
        self.ids.menu_for_transaction_adding.status = 'opened'

    def add_menu_for_a_new_transaction(self):
        self.add_widget(menu_for_a_new_transaction())

    def current_menu_month_name(self):
        return config.current_menu_month_name

    def set_transaction_menu_in(self):
        self.ids.Transaction_menu.ids.my_swiper.add_widget(Transaction_menu_in(name=str(config.current_menu_date)[:-3]))

    def set_categories_menu_buttons(self):
        self.ids.CategoriesMenu.ids.my_swiper.add_widget(
            Categories_buttons_menu(name=str(config.current_menu_date)[:-3]))

    def del_widgets_with_month(self):
        self.ids.CategoriesMenu.ids.my_swiper.clear_widgets()
        self.ids.Transaction_menu.ids.my_swiper.clear_widgets()


class MenuForTransactionAdding(MDNavigationDrawer):
    # the menu opening only in Transaction menu
    # it's needs for choosing what exactly will be in transaction
    # Account, Category of expense and other

    state = OptionProperty("open", options=("close", "open"))
    status = OptionProperty(
        "closed",
        options=(
            "closed",
            "opening_with_swipe",
            "opening_with_animation",
            "opened",
            "closing_with_swipe",
            "closing_with_animation",
        ),
    )
    enable_swiping = BooleanProperty(False)

    def update_status(self, *_) -> None:
        status = self.status
        if status == "closed":
            self.state = "close"
        elif status == "opened":
            self.state = "open"
        elif self.open_progress == 1 and status == "opening_with_animation":
            self.status = "opened"
            self.state = "open"
        elif self.open_progress == 0 and status == "closing_with_animation":
            self.status = "closed"
            self.state = "close"

        elif status in (
                "opening_with_swipe",
                "opening_with_animation",
                "closing_with_swipe",
                "closing_with_animation",
        ):
            pass
        if self.status == "closed":
            self.opacity = 0
        else:
            self.opacity = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # getting data for expense
        self.expense_dict = get_categories_data_from(
            categories_data_file_path='AppData/data_files/categories-data.txt'
        )
        print("# expense_dict", *self.expense_dict.items(), sep='\n')

        # getting data for transfer
        self.transfer = get_accounts_data(
            accounts_data_file_path='AppData/data_files/accounts-data.txt'
        ) | get_savings_data(
            savings_data_file_path='AppData/data_files/savings-data.txt'
        )
        print('# transfer_dict', *self.transfer.items(), sep='\n')

        # adding button to expense tab
        Clock.schedule_once(self.adding_buttons_to_expense_tab)


    def adding_buttons_to_expense_tab(self, *args):
        Clock.schedule_once(self.get_new_func_to_transfer_buttons)

        for button in self.expense_dict.values():
            box = MDScreen(
                md_bg_color=(.8, .3, .4, 1)
            )

            anchor_btn = MDAnchorLayout(md_bg_color=(.3, .6, .4, 1))
            anchor_btn.add_widget(
                MDIconButton(
                    md_bg_color=button['Color'],
                    icon_size="32sp"
                )
            )
            box.add_widget(anchor_btn)

            box.add_widget(
                MDLabel(
                    text=button['Name'],
                    pos_hint={'center_x': .5, 'top': 1},
                    size_hint=(1, .25),
                    halign='center',
                )
            )

            self.ids.expense_layout.add_widget(box)



    def adding_buttons_to_transfer_tab(self, *args):
        for account in self.transfer.values():
            box = MDScreen(
                md_bg_color=(.8, .3, .4, 1)
            )

            anchor_btn = MDAnchorLayout(md_bg_color=(.3, .6, .4, 1))
            anchor_btn.add_widget(
                MDIconButton(
                    md_bg_color=account['Color'],
                    icon_size="32sp"
                )
            )
            box.add_widget(anchor_btn)

            box.add_widget(
                MDLabel(
                    text=account['Name'],
                    pos_hint={'center_x': .5, 'top': 1},
                    size_hint=(1, .25),
                    halign='center',
                )
            )

            self.ids.transfer_layout.add_widget(box)

    def get_new_func_to_transfer_buttons(self, *args):
        for button in self.ids.AccountsMenu_main.ids.accounts_Boxlines.children:
            button.bind(on_press=self.put)

        for button in self.ids.AccountsMenu_main.ids.savings_Boxlines.children:
            button.bind(on_press=self.put)

    def put(self, widget, **kwargs):
        widget.text = 'func is working'
        self.status = 'closed'

        self.parent.add_widget(menu_for_a_new_transaction())
        print(self.parent.children)


class menu_for_a_new_transaction(MDNavigationDrawer):
    # the menu opening, when we know what exactly will be in transaction
    # Account, Category of expense and other
    state = OptionProperty("open", options=("close", "open"))
    status = OptionProperty(
        "opened",
        options=(
            "closed",
            "opening_with_swipe",
            "opening_with_animation",
            "opened",
            "closing_with_swipe",
            "closing_with_animation",
        ),
    )
    enable_swiping = BooleanProperty(False)

    def update_status(self, *_) -> None:
        status = self.status
        if status == "closed":
            self.state = "close"
        elif status == "opened":
            self.state = "open"
        elif self.open_progress == 1 and status == "opening_with_animation":
            self.status = "opened"
            self.state = "open"
        elif self.open_progress == 0 and status == "closing_with_animation":
            self.status = "closed"
            self.state = "close"

            self.del_myself()

        elif status in (
                "opening_with_swipe",
                "opening_with_animation",
                "closing_with_swipe",
                "closing_with_animation",
        ):
            pass
        if self.status == "closed":
            self.opacity = 0
        else:
            self.opacity = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def del_myself(self):
        self.parent.remove_widget(self)


class Manager(ScreenManager):
    pass


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

        # loading multiple .kv files

        # Accounts menu
        Builder.load_file('AppMenus/Accounts_menu/accounts_menu.kv')
        Builder.load_file('AppMenus/Accounts_menu/accounts_menu_main.kv')
        Builder.load_file('AppMenus/Accounts_menu/accounts_menu_debts.kv')
        Builder.load_file('AppMenus/Accounts_menu/accounts_menu_stat.kv')

        # Categories menu
        Builder.load_file('AppMenus/Categories_menu/categories_menu.kv')
        Builder.load_file('AppMenus/Categories_menu/categories_buttons_menu.kv')

        # Transaction menu
        Builder.load_file('AppMenus/Transaction_menu/transaction_menu.kv')
        Builder.load_file('AppMenus/Transaction_menu/transaction_menu_in.kv')
        Builder.load_file('AppMenus/Transaction_menu/date_label_for_transaction_history_menu.kv')
        Builder.load_file('AppMenus/Transaction_menu/menu_for_transaction_adding.kv')

        # main
        Builder.load_file('main_screen.kv')
        Builder.load_file('my_navigation_drawer.kv')
        Builder.load_file('manager.kv')
        Builder.load_file('menu_for_a_new_transaction.kv')

        return Manager()


if __name__ == '__main__':
    # makes empty data files
    create_savings_data_file('AppData/data_files/savings-data.txt')
    create_categories_data_file('AppData/data_files/categories-data.txt')
    create_accounts_data_file('AppData/data_files/accounts-data.txt')
    create_transaction_history_file('AppData/data_files/transaction-history.csv')

    # smartphone screen checking
    Window.size = (0.6 * 640, 0.6 * 1136)

    # start the app
    MoneyStatApp().run()
