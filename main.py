# Kivy and kivymd
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, BooleanProperty, OptionProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

import AppMenus
from AppMenus import menu_for_a_new_transaction, Categories_buttons_menu, \
    Transaction_menu_in, BudgetMenu_in, menu_for_a_new_budget, menu_for_new_or_edit_category

# configuration file
import config

# for reading and writing data
from database import accounts_db_read, categories_db_read
from database.sqlite_db import savings_db_read


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

            # when person start reselection first item, but close the menu not finish
            config.choosing_first_transaction = False

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
        self.expense_dict = categories_db_read()

        # getting data for transfer
        self.transfer = accounts_db_read() | savings_db_read()

        # adding button to expense tab
        Clock.schedule_once(self.adding_buttons_to_expense_tab)

    def adding_buttons_to_expense_tab(self, *args):
        Clock.schedule_once(self.get_new_func_to_transfer_buttons)

        for button_id in self.expense_dict:
            box = MDScreen(
                md_bg_color=(.8, .3, .4, 1)
            )

            anchor_btn = MDAnchorLayout(md_bg_color=(.3, .6, .4, 1))
            anchor_btn.add_widget(
                MDIconButton(
                    id=str(button_id),
                    text=self.expense_dict[button_id]['Name'],
                    md_bg_color=list(self.expense_dict[button_id]['Color'][:-1]) + [1],
                    icon_size="32sp",
                    on_release=self.put
                )
            )
            box.add_widget(anchor_btn)

            box.add_widget(
                MDLabel(
                    text=self.expense_dict[button_id]['Name'],
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
        # closing the old menu
        self.status = 'closed'

        # getting info for a new menu

        # reselection the first item
        if config.choosing_first_transaction:
            if str(widget.id) in self.transfer:
                config.first_transaction_item = {'id': widget.id, 'Name': widget.text, 'Color': widget.md_bg_color,
                                                 'Currency': self.transfer[str(widget.id)]['Currency']}

            config.choosing_first_transaction = False

        # typical selection
        else:
            # first_item
            config.last_transaction_id = list(config.history_dict)[-1]

            last_id = -1
            while not config.history_dict[config.last_transaction_id]['Type'] in ['Transfer', 'Expenses']:
                last_id -= 1
                config.last_transaction_id = list(config.history_dict)[last_id]

            last_transaction = config.history_dict[config.last_transaction_id]

            last_account = last_transaction['From']

            config.first_transaction_item = {'id': last_account,
                                             'Name':
                                                 config.global_accounts_data_dict[last_account]['Name'],
                                             'Color': config.global_accounts_data_dict[last_account]['Color'],
                                             'Currency': last_transaction['FromCurrency']
                                             }
            # second item
            config.second_transaction_item = {'id': widget.id, 'Name': widget.text, 'Color': widget.md_bg_color}

            print(*config.second_transaction_item.items(), sep='\n')

            if str(widget.id) in self.transfer:
                config.second_transaction_item['Currency'] = self.transfer[str(widget.id)]['Currency']

            else:
                config.second_transaction_item['Currency'] = 'RUB'

        # checking
        # print('# first_transaction_item', config.first_transaction_item)
        # print('# second_transaction_item', config.second_transaction_item)

        # adding a new menu to the app
        self.parent.add_widget(menu_for_a_new_transaction())


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

        # Categories menu
        Builder.load_file('AppMenus/Categories_menu/categories_menu.kv')
        Builder.load_file('AppMenus/Categories_menu/categories_buttons_menu.kv')
        Builder.load_file('AppMenus/Categories_menu/Incomes_buttons_menu.kv')

        Builder.load_file('AppMenus/Categories_menu/WaterFill.kv')

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
        Builder.load_file('AppMenus/CashMenus/MenuForAnewBudget.kv')
        Builder.load_file('AppMenus/CashMenus/Menu_for_new_or_edit_category.kv')

        # main
        Builder.load_file('main_screen.kv')
        Builder.load_file('my_navigation_drawer.kv')
        Builder.load_file('manager.kv')

        return Manager()


if __name__ == '__main__':
    # smartphone screen
    Window.size = (0.6 * 640, 0.6 * 1136)

    # start the app
    MoneyStatApp().run()
