from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.properties import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.swiper import MDSwiperItem, MDSwiper
from kivymd.uix.tab import MDTabsBase

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


class CategoriesMenu(MDScreen):

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

    def next_swiper_item(self):
        if self.ids.my_swiper.get_current_index() < len(self.ids.my_swiper.get_items()) - 1:
            print('1')
            self.ids.my_swiper.set_current(self.ids.my_swiper.get_current_index() + 1)

        else:
            print('2')
            # self.ids.my_swiper.add_widget(MDScreen())
class Tab(MDFloatLayout, MDTabsBase):
    pass

class MoneyStatApp(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file('MainScreen.kv')

if __name__ == '__main__':
    MoneyStatApp().run()
