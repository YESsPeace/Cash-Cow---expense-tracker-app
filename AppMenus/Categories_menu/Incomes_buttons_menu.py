from random import choice

from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock

import config

from config import icon_list

from AppMenus.CashMenus.MenuForAnewTransaction import menu_for_a_new_transaction
from AppMenus.Categories_menu.WaterFill import WaterFill
from database import get_transaction_for_the_period, transaction_db_read, budget_data_read, \
    get_incomes_month_data, accounts_db_read, savings_db_read, incomes_db_read


class Incomes_buttons_menu(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # getting data for Incomes
        self.Incomes_menu_button_data_dictionary = incomes_db_read()
        print("# Incomes_menu_button_data_dictionary:", *self.Incomes_menu_button_data_dictionary.items(),
              sep='\n')

        self.get_Incomes_month_data_dict = \
            get_incomes_month_data(get_transaction_for_the_period(
                from_date=str(config.current_menu_date.replace(day=1)),
                to_date=str(config.current_menu_date.replace(day=config.days_in_current_menu_month)),
                history_dict=transaction_db_read()
            )
            )

        print('Incomes_month_Budget_data_dict', *self.get_Incomes_month_data_dict.items(), sep='\n')

        self.Incomes_budget_data_dict = budget_data_read(id='Income_', db_name='budget_data_incomes')

        print('Incomes Budget data',
              *self.Incomes_budget_data_dict.items(),
              sep='\n')

        self.budget_data_date = str(config.current_menu_date)[:-3].replace('-', '')

        if self.budget_data_date in self.Incomes_budget_data_dict:
            print(f'Incomes_Budget_data_dict in BudgetMenu for {self.budget_data_date}',
                  *self.Incomes_budget_data_dict[self.budget_data_date].items(),
                  sep='\n')

        # getting info for a_new_transaction_menu
        self.transfer = accounts_db_read() | savings_db_read()

        Clock.schedule_once(self.button_data_setter, -1)

    def button_data_setter(self, *args):
        for button_id in self.Incomes_menu_button_data_dictionary:
            button = self.Incomes_menu_button_data_dictionary[button_id]

            if self.budget_data_date in self.Incomes_budget_data_dict:

                if (button_id in self.get_Incomes_month_data_dict) and \
                        (button_id in self.Incomes_budget_data_dict[self.budget_data_date]):

                    button_level = int(self.get_Incomes_month_data_dict[button_id]['SUM']) / \
                                   int(self.Incomes_budget_data_dict[self.budget_data_date][button_id]['Budgeted'])

                    print(f'Income level for {button_id}: {button_level}')

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

            self.ids.GridIncomesMenu.add_widget(box)

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
            # second item
            config.last_transaction_id = list(config.history_dict)[-1]

            last_id = -1
            while not config.history_dict[config.last_transaction_id]['Type'] in ['Transfer', 'Expenses']:
                last_id -= 1
                config.last_transaction_id = list(config.history_dict)[last_id]

            last_transaction = config.history_dict[config.last_transaction_id]

            last_account = last_transaction['From']

            config.second_transaction_item = {'id': last_account,
                                             'Name':
                                                 config.global_accounts_data_dict[last_account]['Name'],
                                             'Color': config.global_accounts_data_dict[last_account]['Color'],
                                             'Currency': last_transaction['FromCurrency']
                                             }
            # first item
            config.first_transaction_item = {'id': widget.id,
                                              'Name': self.Incomes_menu_button_data_dictionary[widget.id][
                                                  'Name'],
                                              'Color': self.Incomes_menu_button_data_dictionary[widget.id]
                                                       ['Color'][:-1] + [1]}

            if str(widget.id) in self.transfer:
                config.first_transaction_item['Currency'] = self.transfer[str(widget.id)]['Currency']
            else:
                config.first_transaction_item['Currency'] = 'RUB'

        # adding a new menu to the app
        self.parent.parent.parent.parent.parent.parent.parent.parent.parent.add_widget(menu_for_a_new_transaction())
