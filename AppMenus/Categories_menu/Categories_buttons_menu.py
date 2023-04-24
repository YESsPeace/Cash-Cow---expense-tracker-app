import datetime

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty, StringProperty, DictProperty
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

import config
from AppMenus.BasicMenus import MenuForTransactionAddingBase
from database import get_transaction_for_the_period, transaction_db_read, \
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


class Categories_buttons_menu(MDScreen, MenuForTransactionAddingBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.budget_data_date = str(config.current_menu_date)[:-3].replace('-', '')

        # getting info for a_new_transaction_menu
        Clock.schedule_once(self.refresh_rv_data, 2)

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

    def del_plus_button(self, *args):
        self.ids.GridCategoriesMenu.remove_widget(self.ids.plus_button_categories)
