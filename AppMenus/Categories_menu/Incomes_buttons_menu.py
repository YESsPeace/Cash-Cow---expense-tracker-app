import threading

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import DictProperty, StringProperty, NumericProperty, BooleanProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

import config
from BasicMenus import MenuForTransactionAddingBase
from database import get_transaction_for_the_period, transaction_db_read, budget_data_read, \
    get_incomes_month_data, incomes_db_read


class IncomeItem(MDBoxLayout):
    income_id = StringProperty('income_0')
    button_level = NumericProperty(1)
    category_data = DictProperty(
        {
            'Name': 'default_income',
            'Color': [0, 0, 0, 1],
            'Icon': 'android',
        }
    )


class Incomes_buttons_menu(MDScreen, MenuForTransactionAddingBase):

    data_setting = BooleanProperty(True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.budget_data_date = str(config.current_menu_date)[:-3].replace('-', '')

        # getting info for a_new_transaction_menu
        if self.data_setting is True:
            threading.Thread(target=self.refresh_rv_data, args=(self.category_button_callback,)).start()

    def get_rv_data(self, buttons_callback, *args) -> list:
        out_list = []

        incomes_data = incomes_db_read()

        incomes_month_data_dict = \
            get_incomes_month_data(
                get_transaction_for_the_period(
                    from_date=str(config.current_menu_date.replace(day=1)),
                    to_date=str(config.current_menu_date.replace(day=config.days_in_current_menu_month)),
                    history_dict=transaction_db_read()
                )
            )

        incomes_budget_data_dict = budget_data_read(id='income_', db_name='budget_data_incomes')

        for income_id in incomes_data.keys():
            button_level = 1

            if self.budget_data_date in incomes_budget_data_dict:
                if income_id in incomes_budget_data_dict[self.budget_data_date]:
                    if income_id in incomes_month_data_dict:
                        button_level = int(incomes_month_data_dict[income_id]['SUM']) / \
                                       int(incomes_budget_data_dict[self.budget_data_date][income_id]['Budgeted'])

                    else:
                        button_level = 0

            out_list.append(
                {
                    "viewclass": "CategoryItem",
                    "height": dp(80),
                    "category_id": income_id,
                    "category_data": incomes_data[income_id],
                    "button_level": button_level,
                    "on_release": buttons_callback(income_id)
                }
            )

        return out_list

    def refresh_rv_data(self, buttons_callback=None, *args):
        if not buttons_callback is None:
            new_data = self.get_rv_data(buttons_callback=buttons_callback)

        else:
            new_data = self.get_rv_data(buttons_callback=self.category_button_callback)

        Clock.schedule_once(lambda dt: setattr(self.ids.Incomes_rv, 'data', new_data))

    def category_button_callback(self, category_id):
        return lambda: self.open_menu_for_a_new_transaction(category_id)

    def del_plus_button(self, *args):
        self.ids.GridIncomesMenu.remove_widget(self.ids.plus_button_incomes)