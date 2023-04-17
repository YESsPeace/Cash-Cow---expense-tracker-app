import csv
from calendar import month_name, monthrange

from kivy.graphics import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.properties import OptionProperty, BooleanProperty
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.pickers import MDDatePicker

import config
from AppMenus.Transaction_menu.Transaction_menu_in import Transaction_menu_in
from database import transaction_db_write, transaction_db_read, accounts_and_savings_db_edit_balance

from AppMenus.other_func import calculate, update_month_menu_by_date, update_total_balance_in_UI


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

        if config.second_transaction_item['id'].split('_')[0] == 'categories':
            self.type_ = 'Expenses'

        elif (config.first_transaction_item['id'].split('_')[0] in ['account', 'savings']) and \
                (config.second_transaction_item['id'].split('_')[0] in ['account', 'savings']):
            self.type_ = 'Transfer'

        else:
            self.type_ = 'Income'

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
                                   elevation=0, radius=[0, 0, 0, 0]
                                   )

        date_dialog.bind(on_save=self.change_date)

        date_dialog.open(animation=False)

    def change_date(self, instance, value, date_range):
        self.date_ = '.'.join(str(value).replace('-', '.').split('.')[::-1])
        print(f'Date: type - {type(value)}, {value}; date - {self.date_}')

    def calculate_btn_pressed(self):
        self.ids.sum_label.text = f'{self.currency_first} {calculate(self.ids.sum_label.text)}'

    def write_transaction(self, sum):
        # menu
        self.status = 'closed'

        # getting sum in transaction
        sum = sum[2:]  # del currency

        if sum[-1] == '.':
            sum = sum[:-1]

        try:
            sum = int(sum)

        except ValueError:
            sum = float(sum)

        # the values were got in the __init__
        transaction_ = {}

        transaction_['Date'] = self.date_
        transaction_['Type'] = self.type_
        transaction_['From'] = config.first_transaction_item['id']
        transaction_['To'] = config.second_transaction_item['id']
        transaction_['FromSUM'] = sum
        transaction_['FromCurrency'] = self.code_name_of_first_currency
        transaction_['ToSUM'] = sum
        transaction_['ToCurrency'] = transaction_['FromCurrency']
        transaction_['Comment'] = ''

        if not self.ids.note_input.text == 'notes':
            transaction_['Comment'] = self.ids.note_input.text

        print('# writing transaction:', transaction_)

        # writing
        transaction_db_write(transaction_)

        # updating history_dict
        config.history_dict = transaction_db_read()

        update_month_menu_by_date(
            self,
            date_of_changes=str(self.date_),
            main_menu_id='Transaction_menu',
            month_menu_name=Transaction_menu_in
        )

        update_total_balance_in_UI()
