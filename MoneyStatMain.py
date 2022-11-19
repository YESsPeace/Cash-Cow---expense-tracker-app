from kivy.app import App
from kivy.metrics import dp
from kivy.properties import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

from warnings import warn
from MyWarningMessages import CategoriesDataFileIsNotFounded, AccountsDataFileIsNotFounded

import os

from TxtCategoriesData import create_categories_data_file
from TxtAccountsData import create_accounts_data_file
from CsvTransactionHistory import create_transaction_history_file

# makes empty data files
create_categories_data_file('data_files/categories-data.txt')
create_accounts_data_file('data_files/accounts-data.txt')
create_transaction_history_file('data_files/transaction-history.csv')

class MonthsMenu(BoxLayout):
    pass


def categories_menu_buttons_data(path):
    # this func takes data from categories-data-txt
    categories_menu_button_data_dictionary = {}

    for number_of_button in range(12):
        categories_menu_button_data_dictionary['CategoriesMenu_Button_' + str(number_of_button)] = {}

    try:
        categories_data_file = open(path, 'r+', encoding="UTF8")

        num_of_line_and_button = 0
        for line in categories_data_file:
            name_of_button = line.split('-')[1]
            color_of_button = tuple([float(i) for i in line.split('-')[2][:-1].split(',')])

            categories_menu_button_data_dictionary['CategoriesMenu_Button_' + str(num_of_line_and_button)] = {
                'Name': name_of_button,
                'Color': color_of_button}

            num_of_line_and_button += 1

        categories_data_file.close()

        return categories_menu_button_data_dictionary

    except FileNotFoundError:
        warn('categories_data.txt is not founded. Check if the TxtCategoriesData.py is here',
             CategoriesDataFileIsNotFounded)
        # warning message and return standard list
        return ['ERROR:'.rjust(16) + '\n' + 'File Is Not Founded'.rjust(16) for _ in range(12)]


def accounts_and_savings_data(path):
    data_dict = {"Accounts": {}, "Savings": {}}

    try:
        accounts_and_savings_data_file = open(path, 'r+', encoding="UTF8")

        is_accounts = False
        is_savings = False

        for line in accounts_and_savings_data_file:
            if line.split()[0] == 'accounts':
                is_accounts = True
                is_savings = False

            elif line.split()[0] == 'savings':
                is_accounts = False
                is_savings = True

            elif is_accounts:
                data_list = line.split('-')

                try:
                    data_dict['Accounts'][data_list[0]] = {"Name": data_list[1], "Color": data_list[2],
                                                           'Balance': data_list[3], 'Currency': data_list[4][:-1]}
                except IndexError:
                    continue

            elif is_savings:
                data_list = line.split('-')

                try:
                    data_dict['Savings'][data_list[0]] = {"Name": data_list[1], "Color": data_list[2],
                                                          'Balance': data_list[3], 'Currency': data_list[4][:-1]}
                except IndexError:
                    continue



    except FileNotFoundError:
        warn('accounts_data.txt is not founded. Check if the TxtAccountsData.py is here',
             AccountsDataFileIsNotFounded)

    return data_dict


class AccountsMenu_main(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        self.accounts_and_savings_data_dict = accounts_and_savings_data('data_files/accounts-data.txt')

        print("# accounts_and_savings_data_dictionary:", self.accounts_and_savings_data_dict)

        self.accounts_balance_rub = 0
        self.accounts_balance_usd = 0

        for item in self.accounts_and_savings_data_dict['Accounts'].items():
            if item[1]['Currency'] == "RUB":
                self.accounts_balance_rub += int(item[1]['Balance'])

            elif item[1]['Currency'] == "USD":
                self.accounts_balance_usd += int(item[1]['Balance'])

class AccountsMenu_stat(BoxLayout):
    def click(self):
        self.remove_widget(self.ids.AccountsMenu_stat_label)

class AccountsMenu(BoxLayout):
    pass

class TransactionMenu(BoxLayout):
    pass


class CategoriesMenu(BoxLayout):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        self.categories_menu_button_data_dictionary = categories_menu_buttons_data(
            'data_files/categories-data.txt')
        print("# categories_menu_button_data_dictionary:", self.categories_menu_button_data_dictionary)

        Clock.schedule_once(self.button_data_setter, -1)
    def button_data_setter(self, *args):
        for button_id in self.ids:
            getattr(self.ids, button_id).text = self.categories_menu_button_data_dictionary[button_id]['Name']
            getattr(self.ids, button_id).background_color = self.categories_menu_button_data_dictionary[button_id][
                'Color']


class MainMenuWidget(BoxLayout):
    def top_menu_toggle_button_setter(self, *args):

        self.toggle_button1 = ToggleButton(text='ACCOUNTS', group='sex', state='down', allow_no_selection=False,
                                           on_release=self.switch_accounts_menu_type_to_main)

        self.toggle_button2 = ToggleButton(text='', group='sex', size_hint=(None, 1), width=dp(50),
                                           allow_no_selection=False, background_normal='Icons/statistica.png',
                                           background_down='Icons/statistica_down.png',
                                           on_press=self.switch_accounts_menu_type_to_stat)
    def switch_accounts_menu_type_to_main(self, *args):
        self.ids.AccountsMenu_id.clear_widgets()
        self.ids.AccountsMenu_id.add_widget(self.ids.AccountsMenu_id.ids.AccountsMenu_main_id)
    def switch_accounts_menu_type_to_stat(self, *args):
        self.ids.AccountsMenu_id.clear_widgets()
        self.ids.AccountsMenu_id.add_widget(AccountsMenu_stat())

    def page_layout_swipe_detected(self):
        Clock.schedule_once(self.change_layout_of_page_layuot)

    def change_layout_of_page_layuot(self, *args):
        self.top_menu_toggle_button_setter()
        if self.ids.my_PageLayout.page == 0:
            self.from_any_menus_to_accounts_menu()

        if self.ids.my_PageLayout.page != 0:
            self.return_any_page_layout_from_accounts_menu()

    def return_any_page_layout_from_accounts_menu(self):
        if self.toggle_button1 in self.ids.middle_top_layout.children:
            # removing widgets which were before
            self.ids.middle_top_layout.remove_widget(self.toggle_button1)
            self.ids.middle_top_layout.remove_widget(self.toggle_button2)
            # adding the new toggle buttons
            self.ids.middle_top_layout.add_widget(self.ids.left_btn)
            self.ids.middle_top_layout.add_widget(self.ids.middle_btn)
            self.ids.middle_top_layout.add_widget(self.ids.right_btn)

    def from_any_menus_to_accounts_menu(self):  # change the middle top layout
        if self.ids.middle_btn in self.ids.middle_top_layout.children:
            # removing widgets which were before
            self.ids.middle_top_layout.remove_widget(self.ids.left_btn)
            self.ids.middle_top_layout.remove_widget(self.ids.middle_btn)
            self.ids.middle_top_layout.remove_widget(self.ids.right_btn)
            # adding the new toggle buttons
            self.ids.middle_top_layout.add_widget(self.toggle_button1)
            self.ids.middle_top_layout.add_widget(self.toggle_button2)

    def click_on_month_in_main(self):
        self.ids.top_layout.remove_widget(self.ids.middle_top_layout)
        self.ids.MainMenuWidget.remove_widget(self.ids.my_PageLayout)
        self.ids.MainMenuWidget.remove_widget(self.ids.bottom_navigation_layout)

        self.ids.top_layout_background.height = dp(125 * 0.6)
        self.ids.MainMenuWidget.add_widget(MonthsMenu())
        self.ids.MainMenuWidget.add_widget(self.ids.bottom_navigation_layout)

    def return_page_layout(self):
        if not self.ids.my_PageLayout in self.ids.MainMenuWidget.children:
            self.ids.MainMenuWidget.clear_widgets()

            self.ids.MainMenuWidget.add_widget(self.ids.top_layout_background)
            self.ids.top_layout.add_widget(self.ids.middle_top_layout)
            self.ids.MainMenuWidget.add_widget(self.ids.my_PageLayout)
            self.ids.MainMenuWidget.add_widget(self.ids.bottom_navigation_layout)

            self.ids.top_layout_background.height = dp(125)


class MoneyStatApp(App):
    pass


if __name__ == '__main__':
    MoneyStatApp().run()
