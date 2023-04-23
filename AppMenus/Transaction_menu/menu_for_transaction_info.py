from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty, DictProperty

import config
from AppMenus.BasicMenus import PopUpMenuBase


class menu_for_transaction_info(PopUpMenuBase):
    transaction_id = NumericProperty()

    transaction_data = DictProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self.canvas.before:
            Color(0, 0, 0, .5)
            Rectangle(size=config.main_screen_size, pos=config.main_screen_pos)

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
