from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty, StringProperty, DictProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.weakproxy import WeakProxy
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from random import choice

from kivymd.uix.snackbar import Snackbar

import config
from AppMenus.CashMenus.MenuForAnewTransaction import menu_for_a_new_transaction

from config import icon_list

from database import accounts_db_read, get_transaction_for_the_period, savings_db_read, transaction_db_read, \
    get_categories_month_data, budget_data_read, categories_db_read


class CategoryItem(MDBoxLayout):
    category_id = StringProperty('category_0')
    button_level = NumericProperty(1)
    category_data = DictProperty(
        {
            'Name': 'default_category',
            'Color': [0, 0, 0, 1],
            'Icon': 'android',
        }
    )


class WaterFill(Widget):
    level = NumericProperty(0)
    color = ListProperty([0.2, 0.2, 0.2, 1])


class Categories_buttons_menu(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.budget_data_date = str(config.current_menu_date)[:-3].replace('-', '')

        # getting info for a_new_transaction_menu
        Clock.schedule_once(self.refresh_rv_data)

    def get_rv_data(self, *args) -> list:
        out_list = []

        categories_data = categories_db_read()

        categories_month_data_dict = \
            get_categories_month_data(
                get_transaction_for_the_period(
                    from_date=str(config.current_menu_date.replace(day=1)),
                    to_date=str(config.current_menu_date.replace(day=config.days_in_current_menu_month)),
                    history_dict=transaction_db_read()
                )
            )

        categories_budget_data_dict = budget_data_read(id='categories_', db_name='budget_data_categories')

        for category_id in categories_data.keys():
            button_level = 1

            if self.budget_data_date in categories_budget_data_dict:
                if category_id in categories_budget_data_dict[self.budget_data_date]:
                    if category_id in categories_month_data_dict:
                        button_level = int(categories_month_data_dict[category_id]['SUM']) / \
                                       int(categories_budget_data_dict[self.budget_data_date][category_id]['Budgeted'])

                        print(f'Category level for {category_id}: {button_level}')

                    else:
                        button_level = 0

            out_list.append(
                {
                    "viewclass": "CategoryItem",
                    "height": dp(80),
                    "category_id": category_id,
                    "category_data": categories_data[category_id],
                    "button_level": button_level,
                    "on_release": self.category_button_callback(category_id)
                }
            )

        return out_list

    def refresh_rv_data(self, *args):
        self.ids.Categories_rv.data = self.get_rv_data()

    def category_button_callback(self, category_id):
        return lambda: self.open_menu_for_a_new_transaction(category_id)

    def add_plus_button(self, *args):
        # add plus button, which opening menu for adding a new categories
        app = App.get_running_app()

        plus_button = MDIconButton(
            pos_hint={'center_x': 0.5, 'top': 0.5},
            id='plus_button_categories',
            icon="plus",
            on_release=app.root.ids.main.ids.CategoriesMenu.open_menu_for_edit_categories,
        )

        self.ids.GridCategoriesMenu.add_widget(plus_button)
        self.ids['plus_button_categories'] = WeakProxy(plus_button)

    def del_plus_button(self, *args):
        self.ids.GridCategoriesMenu.remove_widget(self.ids.plus_button_categories)

    def open_menu_for_a_new_transaction(self, widget_id, *args) -> None:
        categories_data = categories_db_read()
        accounts_data = accounts_db_read() | savings_db_read()
        # getting info for a new menu

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
                Snackbar(text="You can't spend money from the category").open()

        # typical selection
        else:
            # first_item
            if len(config.history_dict) > 0:
                config.last_transaction_id = list(config.history_dict)[-1]
                last_transaction = config.history_dict[config.last_transaction_id]

                if last_transaction['Type'] in ['Transfer', 'Expenses']:
                    last_account = last_transaction['From']
                else:
                    last_account = last_transaction['To'][0]


            else:
                last_account = 'account_1'

            config.first_transaction_item = {'id': last_account,
                                             'Name':
                                                 accounts_data[last_account]['Name'],
                                             'Color': accounts_data[last_account]['Color'][:-1],
                                             'Currency': 'RUB'  # last_transaction['FromCurrency']
                                             }
            # second item
            config.second_transaction_item = {'id': widget_id,
                                              'Name': categories_data[widget_id]['Name'],
                                              'Color': categories_data[widget_id]
                                                       ['Color'][:-1]}

            if str(widget_id) in accounts_data:
                config.second_transaction_item['Currency'] = accounts_data[str(widget_id)]['Currency']
            else:
                config.second_transaction_item['Currency'] = 'RUB'

        # adding a new menu to the app
        app = App.get_running_app()

        app.root.ids.main.add_widget(menu_for_a_new_transaction())
