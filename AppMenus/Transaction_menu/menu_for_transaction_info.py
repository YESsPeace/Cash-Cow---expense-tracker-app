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

    def open_menu_for_edit_transaction(self, transaction_id, transaction_data):
        app = App.get_running_app()

        app.root.ids.main.open_menu_for_transaction_adding(transaction_id, transaction_data)
