import threading
from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty, DictProperty

import config
from AppMenus.other_func import update_menus
from BasicMenus import PopUpMenuBase, TopNotification
from database import delete_transaction


class menu_for_transaction_info(PopUpMenuBase):
    transaction_id = NumericProperty()

    transaction_data = DictProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self.canvas.before:
            Color(0, 0, 0, .5)
            Rectangle(size=config.main_screen_size, pos=config.main_screen_pos)

    def delete_button_pressed(self, *args):
        # deleting transaction
        delete_transaction(self.transaction_id)

        # updating menus
        update_menus(self.transaction_data['Date'])

        self.del_myself()

    def edit_date_button_pressed(self, *args):
        TopNotification(text='Will be added in new versions').open()

    def get_data_right_format(self) -> tuple:
        first_transaction_item = (
                {'id': self.transaction_data['From'][0]} | self.transaction_data['From'][1]
        )
        second_transaction_item = (
                {'id': self.transaction_data['To'][0]} | self.transaction_data['To'][1]
        )

        return first_transaction_item, second_transaction_item

    def open_menu_for_edit_transaction(self):
        first_transaction_item, second_transaction_item = self.get_data_right_format()

        app = App.get_running_app()

        app.root.ids.main.add_menu_for_a_new_transaction(
            transaction_id=self.transaction_id,
            transaction_data=self.transaction_data,
            edit_transaction_mode=True,
            first_transaction_item=first_transaction_item,
            second_transaction_item=second_transaction_item

        )

        self.del_myself()
