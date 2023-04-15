from kivy.app import App
from kivymd.uix.screen import MDScreen


class AccountsMenu(MDScreen):
    def open_menu_for_new_account(self, *args):

        app = App.get_running_app()

        app.root.ids.main.add_menu_for_choice_account_type()