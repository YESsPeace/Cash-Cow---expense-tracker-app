from kivy.app import App
from kivy.graphics import Rectangle, Color
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard

import config
from AppMenus.BasicMenus import PopUpMenuBase


class menu_for_choice_new_account_type(PopUpMenuBase):
    new_account = BooleanProperty(True)

    def __init__(self, *args, **kwargs):
        self.account_info = {
            'ID': None,
            'Name': '',
            'Color': [0.71, 0.72, 0.69, 0.5],
            'Balance': 0,
            'Currency': 'RUB',
            'IncludeInTheTotalBalance': 0,
            'Icon': 'card',
            'new': True,
            'type': None
        }
        super().__init__(*args, **kwargs)

        with self.canvas.before:
            Color(0, 0, 0, .5)
            Rectangle(size=config.main_screen_size, pos=config.main_screen_pos)

    def change_type(self, *args):
        print('# account type changed')

        app = App.get_running_app()

        app.root.get_screen('menu_for_new_account').ids.account_type_label.text = self.account_info['type']

        self.del_myself()

    def open_menu_for_new_account(self, *args):
        config.account_info = self.account_info

        app = App.get_running_app()

        app.root.ids.main.add_menu_for_new_account()

        self.del_myself()
