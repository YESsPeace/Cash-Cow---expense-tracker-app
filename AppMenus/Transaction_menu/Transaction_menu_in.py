from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatIconButton, MDIconButton
from kivymd.uix.label import MDLabel
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

        self.current_menu_date_from = config.current_menu_date.replace(day=1)
        self.current_menu_date_to = config.current_menu_date.replace(day=config.days_in_current_menu_month)

        print(self.current_menu_date_from)
        print(config.current_menu_date)

        Clock.schedule_once(self.history_setter_month, 0)

    def history_setter_month(self, *args):
        # the period is current menu month
        # it's from first day of the month to now
        history_dict_for_the_period = get_transaction_for_the_period(
            from_date=str(self.current_menu_date_from),
            to_date=str(self.current_menu_date_to),
            history_dict=self.history_dict
        )
        print(*history_dict_for_the_period.items(), sep='\n')

        if len(history_dict_for_the_period) != 0:
            last_id = list(history_dict_for_the_period)[0]
            config.Transaction_menu_in_last_date = history_dict_for_the_period[last_id]['Date']
            config.last_transaction = history_dict_for_the_period[last_id]

            self.ids.GridLayout_in_ScrollView.add_widget(date_label_for_transaction_history_menu())
            box = MDBoxLayout(orientation='vertical', spacing=dp(1),
                              size_hint=(1, None))

            for transaction in history_dict_for_the_period.values():
                if transaction['Date'] == config.Transaction_menu_in_last_date:
                    try:
                        if transaction['Type'] == 'Expenses':
                            icon_button = MDIconButton(
                                md_bg_color=(config.global_categories_data_dict[transaction['To']]['Color'][:-1] + [1])
                            )

                        else:
                            icon_button = None

                    except KeyError:
                        icon_button = None

                    if transaction['Type'] == 'Expenses':
                        trans_label = MDLabel(text=f"-{transaction['FromSUM']}",
                                              halign='center',
                                              theme_text_color='Custom', text_color=(1, 0, 0, 1),
                                              size_hint_x=None, width=dp(45))

                    elif transaction['Type'] == 'Transfer':
                        trans_label = MDLabel(text=f"{transaction['ToSUM']}",
                                              halign='center',
                                              theme_text_color='Custom', text_color=(1, 1, 1, 1),
                                              size_hint_x=None, width=dp(45))

                    elif transaction['Type'] == 'Income':
                        trans_label = MDLabel(text=f"+{transaction['ToSUM']}",
                                              halign='center',
                                              theme_text_color='Custom', text_color=(0, 1, 0, 1),
                                              size_hint_x=None, width=dp(45))

                    else:
                        trans_label = None

                    box.add_widget(
                        MDBoxLayout(
                            icon_button,
                            MDBoxLayout(
                                MDRectangleFlatIconButton(
                                    text=f"{transaction['From']}\n{transaction['To']}",
                                    icon='',
                                    line_color=(0, 0, 0, 0),
                                    md_bg_color=(.75, .75, .75, 1),
                                    halign='left', size_hint=(1, 1), text_color=(1, 1, 1, 1)
                                ),
                                trans_label
                            ),
                            md_bg_color=(.35, .35, .35, 1)
                        )
                    )

                else:
                    box.height = dp(50) * len(box.children)
                    self.ids.GridLayout_in_ScrollView.add_widget(box)

                    box = MDBoxLayout(orientation='vertical', spacing=dp(1),
                                      size_hint=(1, None))

                    config.Transaction_menu_in_last_date = transaction['Date']

                    self.ids.GridLayout_in_ScrollView.add_widget(date_label_for_transaction_history_menu())

                    try:
                        if transaction['Type'] == 'Expenses':
                            icon_button = MDIconButton(
                                md_bg_color=(
                                            config.global_categories_data_dict[transaction['To']]['Color'][:-1] + [1])
                            )

                        else:
                            icon_button = None

                    except KeyError:
                        icon_button = None

                    if transaction['Type'] == 'Expenses':
                        trans_label = MDLabel(text=f"-{transaction['FromSUM']}",
                                              halign='center',
                                              theme_text_color='Custom', text_color=(1, 0, 0, 1),
                                              size_hint_x=None, width=dp(45))

                    elif transaction['Type'] == 'Transfer':
                        trans_label = MDLabel(text=f"{transaction['ToSUM']}",
                                              halign='center',
                                              theme_text_color='Custom', text_color=(1, 1, 1, 1),
                                              size_hint_x=None, width=dp(45))

                    elif transaction['Type'] == 'Income':
                        trans_label = MDLabel(text=f"+{transaction['ToSUM']}",
                                              halign='center',
                                              theme_text_color='Custom', text_color=(0, 1, 0, 1),
                                              size_hint_x=None, width=dp(45))

                    else:
                        trans_label = None

                    box.add_widget(
                        MDBoxLayout(
                            icon_button,
                            MDBoxLayout(
                                MDRectangleFlatIconButton(
                                    text=f"{transaction['From']}\n{transaction['To']}",
                                    icon='',
                                    line_color=(0, 0, 0, 0),
                                    md_bg_color=(.75, .75, .75, 1),
                                    halign='left', size_hint=(1, 1), text_color=(1, 1, 1, 1)
                                ),
                                trans_label,
                            ),
                            md_bg_color=(.35, .35, .35, 1)
                        )
                    )

            box.height = dp(50) * len(box.children)
            self.ids.GridLayout_in_ScrollView.add_widget(box)
