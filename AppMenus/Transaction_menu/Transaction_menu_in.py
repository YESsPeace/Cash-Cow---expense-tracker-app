from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import DictProperty, NumericProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

import config
from database import get_transaction_for_the_period, categories_db_read, incomes_db_read, accounts_db_read, \
    savings_db_read


class TransactionItem(MDCard):
    radius = [0, 0, 0, 0]
    padding = [dp(5), dp(5), dp(5), dp(5)]
    md_bg_color = [0.12941176470588237, 0.12941176470588237, 0.12941176470588237, 1.0]

    transaction_data = DictProperty()
    transaction_id = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_once(self.set_widget_props)

    def set_widget_props(self, *args):
        if len(self.transaction_data) <= 0:
            return

        transaction_data = self.transaction_data

        self.add_widget(
            MDIconButton(
                icon=str(transaction_data['To']['Icon']),
                md_bg_color=transaction_data['To']['Color'][:-1]
            )
        )

        self.add_widget(
            MDBoxLayout(
                MDLabel(
                    text=str(transaction_data['To']['Name'])
                ),
                MDLabel(
                    text=str(transaction_data['From']['Name'])
                ),
                orientation='vertical',
                padding=[dp(5), 0, 0, 0],
                spacing=dp(1)
            )
        )

        self.add_widget(
            MDLabel(
                text=str(transaction_data['ToSUM']),
                halign='right'
            )
        )

class date_label(MDBoxLayout):
    padding = [dp(5), dp(5), dp(5), dp(5)]
    md_bg_color = [0.12941176470588237, 0.12941176470588237, 0.12941176470588237, 1.0]

    date = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.set_widget_props)

    def set_widget_props(self, *args):
        self.add_widget(
            MDLabel(
                text=str(self.date)
            )
        )

class Transaction_menu_in(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # setting local variable for history dictionary from main Transaction menu
        self.history_dict = config.history_dict
        print(*self.history_dict.items(), sep='\n')

        self.current_menu_date_from = config.current_menu_date.replace(day=1)
        self.current_menu_date_to = config.current_menu_date.replace(day=config.days_in_current_menu_month)

        print(self.current_menu_date_from)
        print(config.current_menu_date)

        Clock.schedule_once(self.set_widget_props)

    def set_widget_props(self, *args):
        Clock.schedule_once(self.history_setter_month)

    def history_setter_month(self, *args):
        history_dict_for_the_period = get_transaction_for_the_period(
            from_date=str(self.current_menu_date_from),
            to_date=str(self.current_menu_date_to),
            history_dict=self.history_dict
        )

        print(*history_dict_for_the_period.items(), sep='\n')

        categories_data = (categories_db_read() | incomes_db_read())
        accounts_data = (accounts_db_read() | savings_db_read())

        self.ids.Transaction_rv.data = []

        last_transaction_date = 'DD.MM.YYYY'

        for transaction_id in history_dict_for_the_period.keys():
            transaction_data = history_dict_for_the_period[transaction_id]

            if transaction_data['Date'] != last_transaction_date:
                last_transaction_date = transaction_data['Date']

                self.ids.Transaction_rv.data.append(
                    {
                        "viewclass": "date_label",
                        "height": dp(40),
                        "orientation": "horizontal",
                        "date": transaction_data['Date'],
                    }
                )


            transaction_data['From'] = (categories_data | accounts_data)[transaction_data['From']]
            transaction_data['To'] = (categories_data | accounts_data)[transaction_data['To']]

            self.ids.Transaction_rv.data.append(
                {
                    "viewclass": "TransactionItem",
                    "height": dp(60),
                    "orientation": "horizontal",
                    "ripple_behavior": True,
                    "transaction_data": transaction_data,
                    "transaction_id": transaction_id
                }
            )
