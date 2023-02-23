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
from AppMenus.CashMenus.MenuForAnewTransaction import menu_for_a_new_transaction, BackGround
from config import icon_list

from AppData.data_scripts.GetData.GetDataFilesData import get_categories_data_from, get_accounts_data, get_savings_data


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

        # getting info for a_new_transaction_menu
        self.transfer = get_accounts_data(
            accounts_data_file_path='AppData/data_files/accounts-data.txt'
        ) | get_savings_data(
            savings_data_file_path='AppData/data_files/savings-data.txt'
        )

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
                size=(dp(47.85555), dp(47.85555))
            ))

            container.add_widget(
                MDIconButton(
                    pos_hint={'center_x': 0.5, 'top': 0.5},
                    id=str(button_id),
                    icon=choice(icon_list),
                    on_release=self.open_menu_for_a_new_transaction,
                )
            )

            box.add_widget(container)

            box.add_widget(
                MDLabel(
                    text=button['Name'],
                    size_hint=(1, .25),
                    halign='center',
                )
            )

            self.ids.GridCategoriesMenu.add_widget(box)

    def open_menu_for_a_new_transaction(self, widget, *args) -> None:
        # getting info for a new menu

        # reselection the first item
        if config.choosing_first_transaction:
            if str(widget.id) in self.transfer:
                config.first_transaction_item = {'id': widget.id, 'Name': widget.text, 'Color': widget.md_bg_color,
                                                 'Currency': self.transfer[str(widget.id)]['Currency']}

            config.choosing_first_transaction = False

        # typical selection
        else:
            # first_item
            config.last_transaction_id = list(config.history_dict)[-1]
            last_transaction = config.history_dict[config.last_transaction_id]

            last_account = last_transaction['From']

            config.first_transaction_item = {'id': last_account,
                                             'Name': config.global_accounts_data_dict[last_account]['Name'],
                                             'Color': config.global_accounts_data_dict[last_account]['Color'],
                                             'Currency': last_transaction['FromCurrency']
                                             }
            # second item
            config.second_transaction_item = {'id': widget.id, 'Name': widget.text, 'Color': widget.md_bg_color}

            if str(widget.id) in self.transfer:
                config.second_transaction_item['Currency'] = self.transfer[str(widget.id)]['Currency']
            else:
                config.second_transaction_item['Currency'] = None

        # checking
        # print('# first_transaction_item', config.first_transaction_item)
        # print('# second_transaction_item', config.second_transaction_item)

        # adding a new menu to the app
        self.parent.parent.add_widget(
            BackGround()
        )
        self.parent.parent.parent.parent.parent.parent.add_widget(menu_for_a_new_transaction())
