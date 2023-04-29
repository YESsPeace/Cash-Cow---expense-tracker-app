import datetime
import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import DictProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen

import config
from database import accounts_db_read, savings_db_read


class AccountsItem(MDCard):
    radius = [0, 0, 0, 0]
    padding = [dp(5), dp(5), dp(5), dp(5)]
    md_bg_color = [0.12941176470588237, 0.12941176470588237, 0.12941176470588237, 1.0]
    spacing = dp(10)
    ripple_behavior = True

    account_id = StringProperty('account_0')

    account_data = DictProperty(
        {
            'Name': 'default_account',
            'Color': [0, 0, 0, 1],
            'Balance': 0.0,
            'Currency': 'RUB',
            'IncludeInTheTotalBalance': 0,
            'Description': 'None',
            'Icon': 'android'
        }
    )


class type_label(MDBoxLayout):
    padding = [dp(5), dp(5), dp(5), dp(5)]
    md_bg_color = [0.12941176470588237, 0.12941176470588237, 0.12941176470588237, 1.0]

    text = StringProperty()


class AccountsMenu_main(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        threading.Thread(target=self.set_accounts).start()

    def on_release_callback(self, account_id):
        return lambda: self.open_menu_for_new_account(account_id)

    def get_accounts_data(self, *args):
        accounts, savings = accounts_db_read(), savings_db_read()
        out_list = []

        for type_name, data_dict in [('Accounts', accounts), ('Savings', savings)]:
            out_list.append(
                {
                    "viewclass": "type_label",
                    "height": dp(40),
                    "orientation": "horizontal",
                    "text": type_name,
                }
            )

            for account_id in data_dict.keys():
                account_data = data_dict[account_id]

                out_list.append(
                    {
                        "viewclass": "AccountsItem",
                        "height": dp(50),
                        "orientation": "horizontal",
                        "account_data": account_data,
                        "account_id": account_id,
                        "on_release": self.on_release_callback(account_id)
                    }
                )

        return out_list

    def set_accounts(self, *args):
        new_data = self.get_accounts_data()

        Clock.schedule_once(lambda dt: setattr(self.ids.accounts_rv, 'data', new_data))

    def open_menu_for_new_account(self, account_id, *args):
        print(account_id)

        self.account_info = (accounts_db_read() | savings_db_read())[account_id]

        self.account_info['ID'] = account_id
        self.account_info['new'] = False
        self.account_info['type'] = 'savings' if account_id.split('_')[0] == 'savings' else 'regular'

        config.account_info = self.account_info

        app = App.get_running_app()

        app.root.ids.main.add_menu_for_new_account()
