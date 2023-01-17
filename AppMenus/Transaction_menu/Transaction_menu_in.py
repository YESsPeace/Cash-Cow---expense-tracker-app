from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.screen import MDScreen

import config
from AppData.data_scripts.GetData.GetHistoryDataForThePeriod import get_transaction_for_the_period
from AppMenus.Transaction_menu.date_label_for_transaction_history_menu import date_label_for_transaction_history_menu


class Transaction_menu_in(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # setting local variable for history dictionary from main Transaction menu
        self.history_dict = config.history_dict
        print(*self.history_dict.items(), sep='\n')

        print(str(config.current_menu_date.replace(day=1)))
        print(str(config.current_menu_date))

        Clock.schedule_once(self.history_setter_month, 0)

    def history_setter_month(self, *args):
        # the period is current menu month
        # it's from first day of the month to now
        history_dict_for_the_period = get_transaction_for_the_period(
            from_date=str(config.current_menu_date.replace(day=1)),
            to_date=str(config.current_menu_date.replace(day=config.days_in_current_menu_month)),
            history_dict=self.history_dict
        )
        print(*history_dict_for_the_period.items(), sep='\n')

        if len(history_dict_for_the_period) != 0:
            last_id = list(history_dict_for_the_period)[-1]
            config.Transaction_menu_in_last_date = history_dict_for_the_period[last_id]['Date']

            self.ids.GridLayout_in_ScrollView.add_widget(date_label_for_transaction_history_menu())
            box = MDBoxLayout(orientation='vertical', padding=dp(5), spacing=dp(5),
                              size_hint=(1, None))

            for transaction in history_dict_for_the_period.values():
                if transaction['Date'] == config.Transaction_menu_in_last_date:
                    box.add_widget(MDRectangleFlatIconButton(
                        text=f"{transaction['Type']}: {transaction['From']['Name']} -> {transaction['To']['Name']}",
                        md_bg_color=transaction['To']['Color'], halign='left',
                        size_hint=(1, 1)
                    ))

                else:
                    box.height = dp(50) * len(box.children)
                    self.ids.GridLayout_in_ScrollView.add_widget(box)

                    box = MDBoxLayout(orientation='vertical', padding=dp(5), spacing=dp(5),
                                      size_hint=(1, None))
                    config.Transaction_menu_in_last_date = transaction['Date']

                    self.ids.GridLayout_in_ScrollView.add_widget(date_label_for_transaction_history_menu())
                    box.add_widget(MDRectangleFlatIconButton(
                        text=f"{transaction['Type']}: {transaction['From']['Name']} -> {transaction['To']['Name']}",
                        md_bg_color=transaction['To']['Color'], halign='left',
                        size_hint=(1, 1)
                    ))

            box.height = dp(50) * len(box.children)
            self.ids.GridLayout_in_ScrollView.add_widget(box)
