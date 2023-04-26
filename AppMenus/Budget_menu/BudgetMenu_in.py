import datetime
from copy import copy

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen

import config
from BasicMenus.CustomWidgets import TopNotification
from database import get_categories_month_data, budget_data_read, \
    transaction_db_read, get_transaction_for_the_period, get_incomes_month_data, \
    incomes_db_read, categories_db_read, savings_db_read, get_savings_month_data


class BudgetItem(MDCard):
    radius = [0, 0, 0, 0]
    padding = [dp(5), dp(5), dp(5), dp(5)]
    md_bg_color = [0.12941176470588237, 0.12941176470588237, 0.12941176470588237, 1.0]
    ripple_behavior = True

    item_id = StringProperty('categories_0')
    item_name = StringProperty('default_budget')
    real_sum = NumericProperty(0)
    budgeted = NumericProperty(1)


class BudgetTitle(MDCard):
    radius = [0, 0, 0, 0]
    padding = [dp(5), dp(5), dp(5), dp(5)]
    # md_bg_color = ListProperty([0.12941176470588237, 0.12941176470588237, 0.12941176470588237, 1.0])

    type_name = StringProperty('default_budget_type')
    real_sum = NumericProperty(0)
    budgeted = NumericProperty(1)


class BudgetMenu_in(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # date
        self.budget_data_date = str(config.current_menu_date)[:-3].replace('-', '')
        self.current_menu_date = config.current_menu_date
        self.days_in_current_menu_month = config.days_in_current_menu_month

        Clock.schedule_once(self.refresh_rv_data, 0.5)

    def get_budget_data(self, *args) -> list:
        out_list = []

        for type_dict, budget_data_dict, month_data_dict, title_text, title_color in [
            (
                    categories_db_read(),  # type_dict
                    budget_data_read(id='categories_', db_name='budget_data_categories'),  # budget_data_dict
                    get_categories_month_data(
                        get_transaction_for_the_period(
                            from_date=str(self.current_menu_date.replace(day=1)),
                            to_date=str(self.current_menu_date.replace(day=self.days_in_current_menu_month)),
                            history_dict=transaction_db_read()
                        )
                    ),  # month_data_dict
                    'Categories',  # title_text
                    [.85, .13, .2, .1],  # title_color
            ),
            (
                    savings_db_read(),  # type_dict
                    budget_data_read(id='savings_', db_name='budget_data_savings'),  # budget_data_dict
                    get_savings_month_data(
                        get_transaction_for_the_period(
                            from_date=str(self.current_menu_date.replace(day=1)),
                            to_date=str(self.current_menu_date.replace(day=self.days_in_current_menu_month)),
                            history_dict=transaction_db_read()
                        )
                    ),  # month_data_dict
                    'Savings',  # title_text
                    [1, .84, 0, .1],  # title_color
            ),
            (
                    incomes_db_read(),  # type_dict
                    budget_data_read(id='income_', db_name='budget_data_incomes'),  # budget_data_dict
                    get_incomes_month_data(
                        get_transaction_for_the_period(
                            from_date=str(self.current_menu_date.replace(day=1)),
                            to_date=str(self.current_menu_date.replace(day=self.days_in_current_menu_month)),
                            history_dict=transaction_db_read()
                        )
                    ),  # month_data_dict
                    'Incomes',  # title_text
                    [.2, .9, .3, .1],  # title_color
            ),
        ]:

            if self.budget_data_date in budget_data_dict:
                budget_data_dict = budget_data_dict[self.budget_data_date]

                out_list.append(
                    {
                        "viewclass": "BudgetTitle",
                        "height": dp(75),
                        "type_name": title_text,
                        "real_sum": sum(month_data_dict[item_id]['SUM'] for item_id in month_data_dict),
                        "budgeted": sum(budget_data_dict[item_id]['Budgeted'] for item_id in budget_data_dict),
                        "md_bg_color": title_color
                    }
                )

                for item_id in budget_data_dict.keys():
                    if item_id in type_dict.keys():
                        real_sum = 0
                        if item_id in month_data_dict:
                            real_sum = month_data_dict[item_id]['SUM']

                        out_list.append(
                            {
                                "viewclass": "BudgetItem",
                                "height": dp(75),
                                "item_id": item_id,
                                "item_name": type_dict[item_id]['Name'],
                                "real_sum": real_sum,
                                "budgeted": budget_data_dict[item_id]['Budgeted'],
                                "on_release": self.on_release_callback(item_id)
                            }
                        )

            else:
                out_list.append(
                    {
                        "viewclass": "BudgetTitle",
                        "height": dp(75),
                        "type_name": title_text,
                        "real_sum": 0,
                        "budgeted": 0,
                        "md_bg_color": title_color
                    }
                )

        return out_list

    def refresh_rv_data(self, *args):
        self.ids.Budget_rv.data = self.get_budget_data()

    def on_release_callback(self, widget_id):
        return lambda: self.open_menu_for_a_new_budget(widget_id=widget_id)

    def open_menu_for_a_new_budget(self, widget_id, *args):
        TopNotification(text='Editing and creating a budget will be in future versions').open()
        return

        widget_type = str(widget_id).split('_')[0].lower()

        budget_data_dict, type_dict, month_data_dict = None, None, None

        if widget_type == 'savings':
            budget_data_dict = budget_data_read(id='savings_', db_name='budget_data_savings')
            type_dict = savings_db_read()

            month_data_dict = \
                get_savings_month_data(
                    get_transaction_for_the_period(
                        from_date=str(self.current_menu_date.replace(day=1)),
                        to_date=str(self.current_menu_date.replace(day=self.days_in_current_menu_month)),
                        history_dict=transaction_db_read()
                    )
                )

        elif widget_type == 'categories':
            budget_data_dict = budget_data_read(id='categories_', db_name='budget_data_categories')
            type_dict = categories_db_read()

            month_data_dict = \
                get_categories_month_data(
                    get_transaction_for_the_period(
                        from_date=str(self.current_menu_date.replace(day=1)),
                        to_date=str(self.current_menu_date.replace(day=self.days_in_current_menu_month)),
                        history_dict=transaction_db_read()
                    )
                )

        elif widget_type == 'income':
            budget_data_dict = budget_data_read(id='income_', db_name='budget_data_incomes')
            type_dict = incomes_db_read()

            month_data_dict = \
                get_incomes_month_data(
                    get_transaction_for_the_period(
                        from_date=str(self.current_menu_date.replace(day=1)),
                        to_date=str(self.current_menu_date.replace(day=self.days_in_current_menu_month)),
                        history_dict=transaction_db_read()
                    )
                )

        if (not budget_data_dict is None) and (not type_dict is None) and not month_data_dict is None:
            date = str(self.budget_data_date).replace('-', '')

            if date in budget_data_dict:
                budget_data_dict = budget_data_dict[date]

            budgeted = budget_data_dict.get(widget_id, {}).get('Budgeted')
            sum = month_data_dict.get(widget_id, {}).get('SUM')

            config.item = {
                'Name': type_dict[widget_id]['Name'],
                'Color': type_dict[widget_id]['Color'],
                'id': widget_id,
                'SUM': sum if not sum is None else 0,
                'Budgeted': budgeted if not budgeted is None else 0,
            }

            app = App.get_running_app()

            app.root.ids.main.add_menu_for_a_new_budget()
