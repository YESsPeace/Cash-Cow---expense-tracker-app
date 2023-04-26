from kivy.app import App
from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen

import config
from AppMenus.Budget_menu.BudgetMenu_in import BudgetMenu_in
from AppMenus.other_func import load_next_month, load_previous_month, get_total_accounts_balance


class BudgetMenu(MDScreen):
    total_accounts_balance = NumericProperty(get_total_accounts_balance())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # just for first creating widgets
        self.current_menu_date = str(config.current_menu_date)[:-3]
        self.current_menu_month_name = config.current_menu_month_name
        self.days_in_month_icon_dict = config.days_in_month_icon_dict
        self.days_in_current_menu_month = config.days_in_current_menu_month

    def update_total_accounts_balance(self, *args):
        self.ids.total_balance_label.text = str(get_total_accounts_balance())

    def load_previous_month(self):
        load_previous_month(self, BudgetMenu_in)

    def load_next_month(self):
        load_next_month(self, BudgetMenu_in)

    def open_menu_for_choice_a_budget_item(self, *args):
        print('open_menu_for_a_new_budget')
        app = App.get_running_app()

        app.root.ids.main.add_menu_for_choice_a_budget_item()
