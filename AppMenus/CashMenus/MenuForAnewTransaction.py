from kivy.graphics import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.properties import NumericProperty, DictProperty, BooleanProperty
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.snackbar import Snackbar

import config
from AppMenus.BasicMenus import PopUpMenuBase
from AppMenus.other_func import calculate, update_total_balance_in_UI, update_menus
from database import transaction_db_write, transaction_db_read


class menu_for_a_new_transaction(PopUpMenuBase):
    first_transaction_item = DictProperty()
    second_transaction_item = DictProperty()

    edit_transaction_mode = BooleanProperty(False)

    transaction_id = NumericProperty()
    transaction_data = DictProperty(
        {
            'Date': '.'.join(item for item in str(config.date_today).split('-')[::-1]),
            'Type': 'Expenses',
            'From': 'account_0',
            'To': 'categories_0',
            'FromSUM': 0,
            'FromCurrency': 'RUB',
            'ToSUM': 0,
            'ToCurrency': 'RUB',
            'Comment': '',
        }
    )

    def __init__(self, *args, **kwargs):
        # default text in calculator
        super().__init__(*args, **kwargs)

        if self.second_transaction_item['id'].split('_')[0] == 'categories':
            self.transaction_data['Type'] = 'Expenses'

        elif (self.first_transaction_item['id'].split('_')[0] in ['account', 'savings']) and \
                (self.second_transaction_item['id'].split('_')[0] in ['account', 'savings']):
            self.transaction_data['Type'] = 'Transfer'

        else:
            self.transaction_data['Type'] = 'Income'

        # just dark background
        with self.canvas.before:
            Color(0, 0, 0, .5)
            Rectangle(size=config.main_screen_size, pos=config.main_screen_pos)

        # setting info for transaction items into widgets
        self.ids.first_item_label.text = self.first_transaction_item['Name']
        self.ids.first_item_label.md_bg_color = self.first_transaction_item['Color']

        self.ids.second_item_label.text = self.second_transaction_item['Name']
        self.ids.second_item_label.md_bg_color = self.second_transaction_item['Color']

    def first_trans_item_pressed(self, *args):
        self.parent.open_menu_for_transaction_adding(
            choosing_first_transaction=True,
            choosing_second_transaction=False,
            second_transaction_item=self.second_transaction_item
        )

        self.del_myself()

    def second_trans_item_pressed(self, *args):
        self.parent.open_menu_for_transaction_adding(
            choosing_first_transaction=False,
            choosing_second_transaction=True,
            first_transaction_item=self.first_transaction_item,
        )

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
        new_date = '.'.join(str(value).replace('-', '.').split('.')[::-1])
        print(f'Date: type - {type(value)}, {value}; date - {new_date}')
        self.transaction_data['Date'] = new_date

    def calculate_btn_pressed(self):
        self.ids.sum_label.text = f'₽ {calculate(self.ids.sum_label.text)}'

    def get_data_right_format(self):
        # getting sum in transaction
        sum = self.ids.sum_label.text[2:]  # del currency

        if sum[-1] == '.':
            sum = sum[:-1]

        try:
            sum = int(sum)

        except ValueError:
            sum = float(sum)

        self.transaction_data['From'] = self.first_transaction_item['id']
        self.transaction_data['To'] = self.second_transaction_item['id']
        self.transaction_data['FromSUM'] = sum
        self.transaction_data['ToSUM'] = sum

        if self.ids.note_input.text != 'notes':
            self.transaction_data['Comment'] = self.ids.note_input.text

    def done_button_pressed(self):
        self.get_data_right_format()

        if self.edit_transaction_mode is True:
            print('self.edit_transaction_mode is True')
            print(self.transaction_id)
            print(*self.transaction_data.items(), sep='\n')

            Snackbar(text='Transaction editing will only in the future').open()

        else:
            self.write_transaction()

    def write_transaction(self):
        # writing
        transaction_db_write(self.transaction_data)
        self.del_myself()

        # updating menus
        update_total_balance_in_UI()
        update_menus(date_of_changes=self.transaction_data['Date'])
