from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from random import choice

import config
from AppData.data_scripts.GetData.Budget_data_scripts.GetCategoriesData import get_categories_budget_data
from AppData.data_scripts.GetData.GetCategoriesMonthData import get_categories_month_data
from AppData.data_scripts.GetData.GetHistoryDataForThePeriod import get_transaction_for_the_period, \
    get_transaction_history
from config import icon_list

from AppData.data_scripts.GetData.GetDataFilesData import get_categories_data_from


class WaterFill(Widget):
    def __init__(self, *args, **kwargs):
        self.level = config.level
        self.color = config.color
        super().__init__(*args, **kwargs)


class Categories_buttons_menu(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # getting data for categories
        self.categories_menu_button_data_dictionary = config.global_categories_data_dict
        print("# categories_menu_button_data_dictionary:", *self.categories_menu_button_data_dictionary.items(),
              sep='\n')

        self.categories_month_data_dict = \
            get_categories_month_data(get_transaction_for_the_period(
                from_date=str(config.current_menu_date.replace(day=1)),
                to_date=str(config.current_menu_date.replace(day=config.days_in_current_menu_month)),
                history_dict=get_transaction_history(
                    history_file_path='AppData/data_files/transaction-history.csv',
                )
            )
            )

        print('Categories_month_Budget_data_dict', *self.categories_month_data_dict.items(), sep='\n')

        self.categories_budget_data_dict = get_categories_budget_data(
            'AppData/data_files/Budget_files/' + str(config.current_menu_date)[:-3] + '/caregories-data.csv'
        )
        if not self.categories_budget_data_dict is None:
            print('Categories_Budget_data_dict in BudgetMenu', *self.categories_budget_data_dict.items(), sep='\n')

        Clock.schedule_once(self.button_data_setter, -1)
    def button_data_setter(self, *args):
        for button_id in self.categories_menu_button_data_dictionary:
            button = self.categories_menu_button_data_dictionary[button_id]

            if (button_id in self.categories_month_data_dict) and \
                    (button_id in self.categories_budget_data_dict):
                config.level = int(self.categories_month_data_dict[button_id]['SUM']) / \
                               int(self.categories_budget_data_dict[button_id]['SUM'])

                if config.level > 1:
                    config.level = 1

            else:
                config.level = 1

            config.color = button['Color']

            box = MDBoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(100)
            )
            container = AnchorLayout()

            container.add_widget(WaterFill(
                pos_hint={'center_x': 0.5, 'top': 1},
                size=(dp(55), dp(55))
            ))

            container.add_widget(MDIconButton(
                pos_hint={'center_x': 0.5, 'top': 0.5},
                id=str(button_id),
                icon=choice(icon_list),
            ))

            box.add_widget(container)

            box.add_widget(
                MDLabel(
                    text=button['Name'],
                    size_hint=(1, .25),
                    halign='center',
                )
            )

            self.ids.GridCategoriesMenu.add_widget(box)
