from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import DictProperty, StringProperty, NumericProperty
from kivy.weakproxy import WeakProxy
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

import config
from AppMenus.CashMenus.MenuForAnewTransaction import menu_for_a_new_transaction
from database import get_transaction_for_the_period, transaction_db_read, budget_data_read, \
    get_incomes_month_data, accounts_db_read, savings_db_read, incomes_db_read


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


class Incomes_buttons_menu(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.budget_data_date = str(config.current_menu_date)[:-3].replace('-', '')

        # getting info for a_new_transaction_menu
        Clock.schedule_once(self.refresh_rv_data)

    def get_rv_data(self, *args) -> list:
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

                        print(f'Category level for {income_id}: {button_level}')

                    else:
                        button_level = 0

            out_list.append(
                {
                    "viewclass": "CategoryItem",
                    "height": dp(80),
                    "category_id": income_id,
                    "category_data": incomes_data[income_id],
                    "button_level": button_level,
                    "on_release": self.category_button_callback(income_id)
                }
            )

        return out_list

    def refresh_rv_data(self, *args):
        self.ids.Incomes_rv.data = self.get_rv_data()

    def category_button_callback(self, category_id):
        return lambda: self.open_menu_for_a_new_transaction(category_id)

    def del_plus_button(self, *args):
        self.ids.GridIncomesMenu.remove_widget(self.ids.plus_button_incomes)

    def open_menu_for_a_new_transaction(self, widget_id, *args) -> None:
        # getting info for a new menu
        incomes_data = incomes_db_read()
        accounts_data = accounts_db_read() | savings_db_read()
        # reselection the first item
        if config.choosing_first_transaction:
            config.choosing_first_transaction = False
            if str(widget_id) in accounts_data:
                config.first_transaction_item = {
                    'id': widget_id,
                    'Name': accounts_data[widget_id]['Name'],
                    'Color': accounts_data[widget_id]['Color'][:-1],
                    'Currency': 'RUB'  # last_transaction['FromCurrency']
                }

            else:
                Snackbar(text="You can't spend money from the income").open()

        # typical selection
        else:
            # second item
            if len(config.history_dict) > 0:
                config.last_transaction_id = list(config.history_dict)[-1]
                last_transaction = config.history_dict[config.last_transaction_id]

                if last_transaction['Type'] in ['Transfer', 'Expenses']:
                    last_account = last_transaction['From']

                    if type(last_account) is tuple:
                        last_account = last_account[0]

                else:
                    last_account = last_transaction['To']

                    if type(last_account) is tuple:
                        last_account = last_account[0]

            else:
                if len(accounts_data) > 0:
                    last_account = 'account_1'

                else:
                    Snackbar(text="Firstly create an account and an expense category").open()
                    return

            config.second_transaction_item = {'id': last_account,
                                              'Name':
                                                  accounts_data[last_account]['Name'],
                                              'Color': accounts_data[last_account]['Color'][:-1],
                                              'Currency': 'RUB'  # last_transaction['FromCurrency']
                                              }
            # first item
            config.first_transaction_item = {
                'id': widget_id,
                'Name': incomes_data[widget_id]['Name'],
                'Color': incomes_data[widget_id]['Color'][:-1]
            }

            if str(widget_id) in accounts_data:
                config.first_transaction_item['Currency'] = accounts_data[str(widget_id)]['Currency']
            else:
                config.first_transaction_item['Currency'] = 'RUB'

        # adding a new menu to the app
        self.parent.parent.parent.parent.parent.parent.parent.parent.parent.add_widget(menu_for_a_new_transaction())
