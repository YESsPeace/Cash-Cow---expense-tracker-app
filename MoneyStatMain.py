from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.properties import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivymd.uix.swiper import MDSwiperItem

from GetDataFilesData import get_accounts_data, get_categories_data_from

from CsvTransactionHistory import create_transaction_history_file
from TxtCategoriesData import create_categories_data_file
from TxtAccountsData import create_accounts_data_file
from TxtSavingsData import create_savings_data_file

# makes empty data files
create_savings_data_file('data_files/savings-data.txt')
create_categories_data_file('data_files/categories-data.txt')
create_accounts_data_file('data_files/accounts-data.txt')
create_transaction_history_file('data_files/transaction-history.csv')

# loading multiple .kv files
Builder.load_file('accounts_menu_stat.kv')
Builder.load_file('accounts_menu_main.kv')
Builder.load_file('accounts_menu.kv')
Builder.load_file('categories_menu.kv')

Window.size = (0.4 * 1080, 0.4 * 2280)


class MonthsMenu(BoxLayout):
    pass


class AccountsMenu_main(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        self.accounts_data_dict = get_accounts_data(
            accounts_data_file_path='data_files/accounts-data.txt')

        print("# accounts_and_savings_data_dictionary:", self.accounts_data_dict)


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

        self.categories_menu_button_data_dictionary = get_categories_data_from(
            categories_data_file_path='data_files/categories-data.txt'
        )
        print("# categories_menu_button_data_dictionary:", self.categories_menu_button_data_dictionary)

        Clock.schedule_once(self.button_data_setter, -1)

    def button_data_setter(self, *args):
        for button_id in self.ids:
            try:
                getattr(self.ids, button_id).text = self.categories_menu_button_data_dictionary[button_id[:-12]]['Name']
                getattr(self.ids, button_id).background_color = \
                    self.categories_menu_button_data_dictionary[button_id[:-12]]['Color']
            except KeyError:
                continue


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

class MoneyStatApp(MDApp):
    pass


if __name__ == '__main__':
    MoneyStatApp().run()
