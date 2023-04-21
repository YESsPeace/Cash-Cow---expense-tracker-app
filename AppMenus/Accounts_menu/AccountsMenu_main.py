from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import DictProperty, NumericProperty, StringProperty
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

import config
from database import accounts_db_read, savings_db_read


class AccountsItem(MDCard):
    radius = [0, 0, 0, 0]
    padding = [dp(5), dp(5), dp(5), dp(5)]
    md_bg_color = [0.12941176470588237, 0.12941176470588237, 0.12941176470588237, 1.0]
    spacing = dp(10)
    ripple_behavior = True

    account_data = DictProperty()
    account_id = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_once(self.set_widget_props)

    def set_widget_props(self, *args):
        account_data = self.account_data

        self.add_widget(
            MDAnchorLayout(
                MDIconButton(
                    icon=str(account_data['Icon']),
                ),
                size_hint_x=None,
                width=dp(60),
                padding=dp(20),
                md_bg_color=account_data['Color'],
            )
        )

        self.add_widget(
            MDLabel(
                text=str(account_data['Name'])
            )
        )

        self.add_widget(
            MDLabel(
                text=str(account_data['Balance']),
                halign='right'
            )
        )


class type_label(MDBoxLayout):
    padding = [dp(5), dp(5), dp(5), dp(5)]
    md_bg_color = [0.12941176470588237, 0.12941176470588237, 0.12941176470588237, 1.0]

    text = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.set_widget_props)

    def set_widget_props(self, *args):
        self.add_widget(
            MDLabel(
                text=str(self.text)
            )
        )


class AccountsMenu_main(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.accounts_data_dict = config.global_accounts_data_dict

        self.savings_data_dict = config.global_savings_data_dict

        print("# accounts_data_dictionary:", self.accounts_data_dict)
        print('# savings_data_dictionary:', self.savings_data_dict)

        Clock.schedule_once(self.set_widget_props)

    def set_widget_props(self, *args):
        Clock.schedule_once(self.set_accounts)

    def set_accounts(self, *args):
        accounts, savings = accounts_db_read(), savings_db_read()
        self.ids.accounts_rv.data = []

        for type_name, data_dict in [('Accounts', accounts), ('Savings', savings)]:
            self.ids.accounts_rv.data.append(
                {
                    "viewclass": "type_label",
                    "height": dp(40),
                    "orientation": "horizontal",
                    "text": type_name,
                }
            )

            for account_id in data_dict.keys():
                account_data = data_dict[account_id]

                self.ids.accounts_rv.data.append(
                    {
                        "viewclass": "AccountsItem",
                        "height": dp(50),
                        "orientation": "horizontal",
                        "account_data": account_data,
                        "account_id": account_id,
                        "on_release": self.on_release_callback(account_id)
                    }
                )

    def on_release_callback(self, account_id):
        return lambda: self.open_menu_for_new_account(account_id)

    def open_menu_for_new_account(self, account_id, *args):
        print(account_id)

        self.account_info = (accounts_db_read() | savings_db_read())[account_id]

        self.account_info['ID'] = account_id
        self.account_info['new'] = False
        self.account_info['type'] = 'savings' if account_id.split('_')[0] == 'savings' else 'regular'

        config.account_info = self.account_info

        app = App.get_running_app()

        app.root.ids.main.add_menu_for_new_account()
