from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from random import choice

import config
from AppMenus.CashMenus.MenuForAnewTransaction import menu_for_a_new_transaction

from config import icon_list

from database import accounts_db_read, get_transaction_for_the_period, savings_db_read, transaction_db_read, \
    get_categories_month_data, budget_data_read, categories_db_read

from AppMenus.Categories_menu.WaterFill import WaterFill


class Categories_buttons_menu(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # getting data for categories
        self.categories_menu_button_data_dictionary = categories_db_read()
        print("# categories_menu_button_data_dictionary:", *self.categories_menu_button_data_dictionary.items(),
              sep='\n')

        self.categories_month_data_dict = \
            get_categories_month_data(get_transaction_for_the_period(
                from_date=str(config.current_menu_date.replace(day=1)),
                to_date=str(config.current_menu_date.replace(day=config.days_in_current_menu_month)),
                history_dict=transaction_db_read()
            )
            )

        print('Categories_month_Budget_data_dict', *self.categories_month_data_dict.items(), sep='\n')

        self.categories_budget_data_dict = budget_data_read(id='Categories_', db_name='budget_data_categories')

        print('Categories Budget data',
              *self.categories_budget_data_dict.items(),
              sep='\n')

        self.budget_data_date = str(config.current_menu_date)[:-3].replace('-', '')

        if self.budget_data_date in self.categories_budget_data_dict:
            print(f'Categories_Budget_data_dict in BudgetMenu for {self.budget_data_date}',
                  *self.categories_budget_data_dict[self.budget_data_date].items(),
                  sep='\n')

        # getting info for a_new_transaction_menu
        self.transfer = accounts_db_read() | savings_db_read()

        Clock.schedule_once(self.button_data_setter, -1)

    def button_data_setter(self, *args):
        for button_id in self.categories_menu_button_data_dictionary:
            button = self.categories_menu_button_data_dictionary[button_id]

            if (self.budget_data_date in self.categories_budget_data_dict) and \
                    (button_id in self.categories_budget_data_dict[self.budget_data_date]):

                if button_id in self.categories_month_data_dict:

                    button_level = int(self.categories_month_data_dict[button_id]['SUM']) / \
                                   int(self.categories_budget_data_dict[self.budget_data_date][button_id]['Budgeted'])

                else:
                    button_level = 0

                if button_level > 1:
                    button_level = 1

            else:
                button_level = 1

            if 'Icon' in button:
                b_icon = button['Icon']

            else:
                b_icon = choice(icon_list)

            box = MDBoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(100)
            )
            container = AnchorLayout()

            container.add_widget(WaterFill(
                pos_hint={'center_x': 0.5, 'top': 1},
                size=(dp(47.85555), dp(47.85555)),
                level=button_level,
                color=button['Color']

            ))

            container.add_widget(
                MDIconButton(
                    pos_hint={'center_x': 0.5, 'top': 0.5},
                    id=str(button_id),
                    icon=b_icon,
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

            last_id = -1
            while not config.history_dict[config.last_transaction_id]['Type'] in ['Transfer', 'Expenses']:
                last_id -= 1
                config.last_transaction_id = list(config.history_dict)[last_id]

            last_transaction = config.history_dict[config.last_transaction_id]

            last_account = last_transaction['From']

            config.first_transaction_item = {'id': last_account,
                                             'Name':
                                                 config.global_accounts_data_dict[last_account]['Name'],
                                             'Color': config.global_accounts_data_dict[last_account]['Color'],
                                             'Currency': last_transaction['FromCurrency']
                                             }
            # second item
            config.second_transaction_item = {'id': widget.id,
                                              'Name': self.categories_menu_button_data_dictionary[widget.id]['Name'],
                                              'Color': self.categories_menu_button_data_dictionary[widget.id]
                                                       ['Color'][:-1] + [1]}

            if str(widget.id) in self.transfer:
                config.second_transaction_item['Currency'] = self.transfer[str(widget.id)]['Currency']
            else:
                config.second_transaction_item['Currency'] = 'RUB'

        # adding a new menu to the app
        app = App.get_running_app()

        app.root.ids.main.add_widget(menu_for_a_new_transaction())
