import csv
import datetime

from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.lang import Builder
from kivy.properties import ObjectProperty, BooleanProperty, OptionProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.color_definitions import hue
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import BaseDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.pickers.datepicker import BaseDialogPicker
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
            last_transaction = config.history_dict[config.last_transaction_id]

            last_account = last_transaction['From']

            config.first_transaction_item = {'id': last_account,
                                             'Name': config.global_accounts_data_dict[last_account]['Name'],
                                             'Color': config.global_accounts_data_dict[last_account]['Color'],
                                             'Currency': last_transaction['FromCurrency']
                                             }
            # second item
            config.second_transaction_item = {'id': widget.id, 'Name': widget.text, 'Color': widget.md_bg_color}

            if str(widget.id) in self.transfer:
                config.second_transaction_item['Currency'] = self.transfer[str(widget.id)]['Currency']
            else:
                config.second_transaction_item['Currency'] = None

        # checking
        print('# first_transaction_item', config.first_transaction_item)
        print('# second_transaction_item', config.second_transaction_item)

        # adding a new menu to the app
        self.parent.add_widget(menu_for_a_new_transaction())


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
        # getting currency code name like 'USD'
        # the first item is from last transaction account in class transaction menu
        self.code_name_of_first_currency = config.first_transaction_item['Currency']
        # the second is from the pressed button in class MenuForTransactionAdding
        self.code_name_of_second_currency = config.second_transaction_item['Currency']
        print(f'from: {self.code_name_of_first_currency}; to: {self.code_name_of_second_currency}')

        # getting symbol of the currency like 'USD' = '$'
        self.currency_first = config.currency_symbol_dict[self.code_name_of_first_currency]
        self.second_currency = config.currency_symbol_dict[self.code_name_of_second_currency]
        print(f'from: {self.currency_first}; to: {self.second_currency}')

        # default text in calculator
        self.default_sum_label_text = f'{self.currency_first} 0'

        # transaction value to write
        # default value for a transaction
        self.date_ = str(config.date_today).split('-')[::-1]  # default value
        self.date_ = '.'.join(item for item in self.date_)

        # getting type of transaction
        self.type_ = None
        if config.second_transaction_item['id'].split('_')[0] == 'Categories':
            self.type_ = 'Expenses'
        elif config.first_transaction_item['id'].split('_')[0] == config.second_transaction_item['id'].split('_')[0]:
            self.type_ = 'Transfer'

        # after creating all kivy widgets
        super().__init__(*args, **kwargs)

        # just dark background
        with self.canvas.before:
            Color(0, 0, 0, .5)
            Rectangle(size=config.main_screen_size, pos=config.main_screen_pos)

        # setting info for transaction items into widgets
        self.ids.first_item_label.text = config.first_transaction_item['Name']
        self.ids.first_item_label.md_bg_color = config.first_transaction_item['Color']

        self.ids.second_item_label.text = config.second_transaction_item['Name']
        self.ids.second_item_label.md_bg_color = config.second_transaction_item['Color']

    def del_myself(self):
        self.parent.remove_widget(self)

    def first_trans_item_pressed(self, *args):
        print('FIRST')
        config.first_transaction_item = None

        self.parent.open_menu_for_transaction_adding()

        self.parent.ids.menu_for_transaction_adding.ids.tab_manager.switch_to(
            self.parent.ids.menu_for_transaction_adding.ids.transfer_tab, do_scroll=False)

        config.choosing_first_transaction = True

        self.del_myself()

    def second_trans_item_pressed(self, *args):
        print('SECOND')

        self.parent.open_menu_for_transaction_adding()

        self.parent.ids.menu_for_transaction_adding.ids.tab_manager.switch_to(
            self.parent.ids.menu_for_transaction_adding.ids.expense_tab, do_scroll=False)

        self.del_myself()

    def sign_btn_pressed(self, btn):
        if len(set(self.ids.sum_label.text).intersection({'+', '-', '÷', 'x'})):
            self.calculate_btn_pressed()
            self.ids.sum_label.text = self.ids.sum_label.text + btn.text

        elif self.ids.sum_label.text[-1] in ['+', '-', '÷', 'x']:
            self.ids.sum_label.text = self.ids.sum_label.text[:-1] + btn.text

        else:
            self.ids.sum_label.text = self.ids.sum_label.text + btn.text

        self.ids.done_btn.text = '='

    def show_date_picker(self):
        date_dialog = MDDatePicker(year=config.current_year, month=config.current_month, day=config.current_day,
                                   primary_color=(.6, .1, .2, 1), accent_color=(.15, .15, .15, 1),
                                   selector_color=(.6, .1, .2, 1), text_color=(1, 1, 1, 1),
                                   text_current_color=(.9, .15, .3, 1), text_button_color=(1, 1, 1, 1),
                                   radius=[0, 0, 0, 0], elevation=0, shadow_softness=0, shadow_offset=(0, 0),
                                   )

        date_dialog.bind(on_save=self.change_date)

        date_dialog.open()

    def change_date(self, instance, value, date_range):
        self.date_ = '.'.join(str(value).replace('-', '.').split('.')[::-1])
        print(f'Date: type - {type(value)}, {value}; date - {self.date_}')

    def calculate_btn_pressed(self):
        self.ids.sum_label.text = f'{self.currency_first} {self.calculate_it(self.ids.sum_label.text)}'

    def calculate_it(self, expression):
        if '+' in expression:
            num_1, num_2 = expression.split('+')
            answer = float(num_1[2:]) + float(num_2)
            answer = float("{:.2f}".format(answer))
            if answer % 1 == 0:
                answer = int(answer)

            return str(answer)

        elif '-' in expression:
            num_1, num_2 = expression.split('-')
            answer = float(num_1[2:]) - float(num_2)
            answer = float("{:.2f}".format(answer))
            if answer % 1 == 0:
                answer = int(answer)

            return str(answer)

        elif '÷' in expression:
            num_1, num_2 = expression.split('÷')
            answer = float(num_1[2:]) / float(num_2)
            answer = float("{:.2f}".format(answer))
            if answer % 1 == 0:
                answer = int(answer)

            return str(answer)

        elif 'x' in expression:
            num_1, num_2 = expression.split('x')
            answer = float(num_1[2:]) * float(num_2)
            answer = float("{:.2f}".format(answer))
            if answer % 1 == 0:
                answer = int(answer)

            return str(answer)

        else:
            return False

    def write_transaction(self, sum):
        # menu
        self.status = 'closed'

        print(self.parent.ids.screen3.ids)

        self.parent.ids.screen3.clear_widgets()

        self.parent.ids.screen3.add_widget(Transaction_menu())

        # getting sum in transaction
        sum = sum[2:]  # del currency

        if sum[-1] == '.':
            sum = sum[:-1]
        if sum == str(int(sum)):
            sum = int(sum)
        else:
            sum = float(sum)

        # the values were got in the __init__
        transaction_ = {}
        transaction_['id'] = int(config.last_transaction_id) + 1
        config.last_transaction_id = str(transaction_['id'])
        transaction_['Date'] = self.date_
        transaction_['Type'] = self.type_
        transaction_['From'] = config.first_transaction_item['id']
        transaction_['To'] = config.second_transaction_item['id']
        transaction_['FromSUM'] = sum
        transaction_['FromCurrency'] = self.code_name_of_first_currency
        transaction_['ToSUM'] = sum
        transaction_['ToCurrency'] = transaction_['FromCurrency']

        if not self.ids.note_input.text == 'notes':
            transaction_['Comment'] = self.ids.note_input.text

        print('# writing transaction:', transaction_)

        # writing
        with open('AppData/data_files/transaction-history.csv',
                  encoding='utf-8', mode='a+', newline='') as history_file:
            writer = csv.writer(history_file, delimiter=',')

            writer.writerow(transaction_.values())

        # updating history_dict

        config.history_dict[transaction_['id']] = {
            'Date': transaction_['Date'],
            'Type': transaction_['Type'],
            'From': transaction_['From'],
            'To': transaction_['To'],
            'FromSUM': transaction_['FromSUM'],
            'FromCurrency': transaction_['FromCurrency'],
            'ToSUM': transaction_['ToSUM'],
            'ToCurrency': transaction_['ToCurrency']
        }


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
