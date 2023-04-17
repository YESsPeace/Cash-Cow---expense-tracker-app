from kivy.app import App
from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen

from AppMenus.other_func import get_total_accounts_balance


class AccountsMenu(MDScreen):
    total_accounts_balance = NumericProperty(get_total_accounts_balance())

    def open_menu_for_new_account(self, *args):
        app = App.get_running_app()

        app.root.ids.main.add_menu_for_choice_account_type()

    def update_total_accounts_balance(self, *args):
        self.ids.total_balance_label.text = str(get_total_accounts_balance())
