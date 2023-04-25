import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import DictProperty, NumericProperty, StringProperty, ListProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen

import config
from database import get_transaction_for_the_period, categories_db_read, incomes_db_read, accounts_db_read, \
    savings_db_read, transaction_db_read


class TransactionItem(MDCard):
    radius = [0, 0, 0, 0]
    padding = [dp(5), dp(5), dp(5), dp(5)]
    md_bg_color = [0.12941176470588237, 0.12941176470588237, 0.12941176470588237, 1.0]
    ripple_behavior = True
    orientation = "horizontal"

    transaction_id = NumericProperty(0)
    sign = StringProperty('')
    color = ListProperty([1, 1, 1])

    transaction_data = DictProperty(
        {
            'Date': '18.04.2023',
            'Type': 'Expenses',
            'From': (
                'account_0',
                {
                    'Name': 'default_account',
                    'Color': [0, 0, 0, 1],
                    'Balance': 0.0,
                    'Currency': 'RUB',
                    'IncludeInTheTotalBalance': 0,
                    'Description': 'None',
                    'Icon': 'android'
                }
            ),
            'To': (
                'category_0',
                {
                    'Name': 'default_category',
                    'Color': [0, 0, 0, 1],
                    'Icon': 'android'
                }
            ),
            'FromSUM': '9999',
            'FromCurrency': 'RUB',
            'ToSUM': '9999',
            'ToCurrency': 'RUB',
            'Comment': ''
        }
    )


class date_label(MDBoxLayout):
    padding = [dp(5), dp(5), dp(5), dp(5)]
    md_bg_color = [0.12941176470588237, 0.12941176470588237, 0.12941176470588237, 1.0]

    date = StringProperty()


class Transaction_menu_in(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        Clock.schedule_once(self.refresh_rv_data, 0.5)

    def get_rv_data(self, *args) -> list:
        out_list = []

        history_dict_for_the_period = get_transaction_for_the_period(
            from_date=str(config.current_menu_date.replace(day=1)),
            to_date=str(config.current_menu_date.replace(day=config.days_in_current_menu_month)),
            history_dict=transaction_db_read()
        )

        categories_data = (categories_db_read() | incomes_db_read())
        accounts_data = (accounts_db_read() | savings_db_read())

        last_transaction_date = 'DD.MM.YYYY'

        for transaction_id in history_dict_for_the_period.keys():
            transaction_data = history_dict_for_the_period[transaction_id]

            transaction_data['From'] = (transaction_data['From'],
                                        (categories_data | accounts_data).get((transaction_data['From'])))

            transaction_data['To'] = (transaction_data['To'],
                                      (categories_data | accounts_data).get(transaction_data['To']))

            if transaction_data['Date'] != last_transaction_date:
                last_transaction_date = transaction_data['Date']

                out_list.append(
                    {
                        "viewclass": "date_label",
                        "height": dp(40),
                        "orientation": "horizontal",
                        "date": transaction_data['Date'],
                    }
                )

            if (transaction_data['From'][1] is not None) and (transaction_data['To'][1] is not None):
                out_list.append(
                    {
                        "viewclass": "TransactionItem",
                        "height": dp(60),
                        "transaction_data": transaction_data,
                        "transaction_id": transaction_id,
                        "sign": config.transaction_color[transaction_data['Type']][0],
                        "color": config.transaction_color[transaction_data['Type']][1],
                        "on_release": self.on_transaction_item_callback(transaction_id, transaction_data)
                    }
                )

        return out_list

    def refresh_rv_data(self, *args):
        new_data = self.get_rv_data()

        if len(new_data) < 1:
            new_data.append(
                {
                    "viewclass": "date_label",
                    "height": dp(40),
                    "orientation": "horizontal",
                    "date": "There's no transactions in this month",
                }
            )

        self.ids.Transaction_rv.data = new_data

    def on_transaction_item_callback(self, transaction_id, transaction_data, *args):
        return lambda: self.open_menu_for_transaction_info(transaction_id, transaction_data)

    def open_menu_for_transaction_info(self, transaction_id, transaction_data, *args):
        app = App.get_running_app()

        app.root.ids.main.open_menu_for_transaction_info(transaction_id, transaction_data)
