from kivy.graphics import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.properties import NumericProperty, DictProperty
from kivymd.uix.pickers import MDDatePicker

import config
from AppMenus.BasicMenus import PopUpMenuBase
from AppMenus.other_func import calculate, update_total_balance_in_UI, update_menus
from database import transaction_db_write, transaction_db_read


class menu_for_a_new_transaction(PopUpMenuBase):
    first_transaction_item = DictProperty()
    second_transaction_item = DictProperty()

    transaction_id = NumericProperty()
    transaction_data = DictProperty()

    def __init__(self, *args, **kwargs):
        # default text in calculator
        self.default_sum_label_text = f'₽ 0'

        super().__init__(*args, **kwargs)

        # transaction value to write
        # default value for a transaction
        self.date_ = str(config.date_today).split('-')[::-1]  # default value
        self.date_ = '.'.join(item for item in self.date_)

        # getting type of transaction
        self.type_ = None

        if self.second_transaction_item['id'].split('_')[0] == 'categories':
            self.type_ = 'Expenses'

        elif (self.first_transaction_item['id'].split('_')[0] in ['account', 'savings']) and \
                (self.second_transaction_item['id'].split('_')[0] in ['account', 'savings']):
            self.type_ = 'Transfer'

        else:
            self.type_ = 'Income'

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
        print('FIRST')
        self.parent.open_menu_for_transaction_adding(
            choosing_first_transaction=True,
            choosing_second_transaction=False,
            second_transaction_item=self.second_transaction_item
        )

        self.del_myself()

    def second_trans_item_pressed(self, *args):
        print('SECOND')

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
        self.date_ = '.'.join(str(value).replace('-', '.').split('.')[::-1])
        print(f'Date: type - {type(value)}, {value}; date - {self.date_}')

    def calculate_btn_pressed(self):
        self.ids.sum_label.text = f'₽ {calculate(self.ids.sum_label.text)}'

    def done_button_pressed(self):
        self.write_transaction(self.ids.sum_label.text)

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
        transaction_['From'] = self.first_transaction_item['id']
        transaction_['To'] = self.second_transaction_item['id']
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

        update_total_balance_in_UI()

        update_menus(date_of_changes=self.date_)
