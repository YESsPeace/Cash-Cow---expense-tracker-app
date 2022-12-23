from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import Clock, ObjectProperty
from kivy.core.window import Window
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

import datetime
from calendar import monthrange, month_name

from AppData.data_scripts.GetData.GetDataFilesData import get_accounts_data, get_categories_data_from, get_savings_data

from AppData.data_scripts.Creating_data_files.CsvTransactionHistory import create_transaction_history_file
from AppData.data_scripts.Creating_data_files.TxtCategoriesData import create_categories_data_file
from AppData.data_scripts.Creating_data_files.TxtAccountsData import create_accounts_data_file
from AppData.data_scripts.Creating_data_files.TxtSavingsData import create_savings_data_file


class AccountsMenu(Screen):
    pass


class AccountsMenu_main(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        self.accounts_data_dict = get_accounts_data(
            accounts_data_file_path='AppData/data_files/accounts-data.txt'
        )
        self.savings_data_dict = get_savings_data(
            savings_data_file_path='AppData/data_files/savings-data.txt'
        )

        print("# accounts_data_dictionary:", self.accounts_data_dict)
        print('# savings_data_dictionary:', self.savings_data_dict)

        Clock.schedule_once(self.adding_accountsANDsavings_main_menu, -1)

    def adding_accountsANDsavings_main_menu(self, *args):
        for account_id in self.accounts_data_dict:
            my_widget = Button(background_color=(.1, .8, .9, 1), background_normal='')

            self.ids.accounts_Boxlines.add_widget(my_widget)

class AccountsMenu_debts(MDScreen):
    pass


class AccountsMenu_stat(MDScreen):
    def click(self):
        self.remove_widget(self.ids.AccountsMenu_stat_label)


class CategoriesMenu(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        # just for first creating widgets
        self.current_menu_month_name = current_menu_month_name
        self.days_in_month_icon_dict = days_in_month_icon_dict
        self.days_in_current_menu_month = days_in_current_menu_month

    def load_previous_month(self):
        global current_menu_date, days_in_current_menu_month, current_menu_month_name

        last_month_date = current_menu_date - datetime.timedelta(days=days_in_current_menu_month)
        # print('Year:', last_month_date.strftime("%Y") + ',', 'Month:', last_month_date.strftime("%m"))

        # update data in python
        current_menu_date = last_month_date

        days_in_current_menu_month = monthrange(current_menu_date.year, current_menu_date.month)[1]
        current_menu_month_name = month_name[current_menu_date.month]

        # update data in menu
        self.ids.month_label.text = current_menu_month_name
        self.ids.month_label.icon = days_in_month_icon_dict[days_in_current_menu_month]

        if self.ids.my_swiper.index == 0:
            self.ids.my_swiper.add_widget(Categories_buttons_menu(name=last_month_date.strftime("%Y") + '.' +
                                                                       last_month_date.strftime("%m")), index=-1)
            # current_menu_month_name
            self.ids.my_swiper.index = 1
            print('After-previous', self.ids.my_swiper.slides)

        self.ids.my_swiper.index = self.ids.my_swiper.index - 1

        # self.ids.my_swiper.load_previous()

    def load_next_month(self):
        global current_menu_date, days_in_current_menu_month, current_menu_month_name

        # getting next month
        next_month_date = current_menu_date + datetime.timedelta(days=days_in_current_menu_month)
        # print('Year:', next_month_date.strftime("%Y") + ',', 'Month:', next_month_date.strftime("%m"))

        # update data in python
        current_menu_date = next_month_date

        days_in_current_menu_month = monthrange(current_menu_date.year, current_menu_date.month)[1]
        current_menu_month_name = month_name[current_menu_date.month]

        # update data in menu
        self.ids.month_label.text = current_menu_month_name
        self.ids.month_label.icon = days_in_month_icon_dict[days_in_current_menu_month]

        if self.ids.my_swiper.index == len(self.ids.my_swiper.slides) - 1:
            self.ids.my_swiper.add_widget(Categories_buttons_menu(name=next_month_date.strftime("%Y") + '.' +
                                                                       next_month_date.strftime("%m")))
            # current_menu_month_name
            print('After-next', self.ids.my_swiper.slides)

        self.ids.my_swiper.index = self.ids.my_swiper.index + 1

        # self.ids.my_swiper.load_next()


class Categories_buttons_menu(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        # getting data for categories
        self.categories_menu_button_data_dictionary = get_categories_data_from(
            categories_data_file_path='AppData/data_files/categories-data.txt'
        )
        print("# categories_menu_button_data_dictionary:", self.categories_menu_button_data_dictionary)

        Clock.schedule_once(self.button_data_setter, -1)

    def button_data_setter(self, *args):
        for button_id in self.ids:
            try:
                getattr(self.ids, button_id).text = \
                    self.categories_menu_button_data_dictionary[button_id[:-12]]['Name']
                getattr(self.ids, button_id).background_color = \
                    self.categories_menu_button_data_dictionary[button_id[:-12]]['Color']
            except KeyError:
                continue


class Transaction_menu(MDScreen):
    pass

class MainSrceen(MDScreen):
    pass


class Manager(ScreenManager):
    pass


class MyNavigationDrawer(MDNavigationDrawer):
    def open_main(self):
        print(1)

    def open_other(self):
        print(2)


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class MoneyStatApp(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"

        # loading multiple .kv files
        Builder.load_file('AppMenus/Accounts_menu/accounts_menu_stat.kv')
        Builder.load_file('AppMenus/Accounts_menu/accounts_menu_main.kv')
        Builder.load_file('AppMenus/Accounts_menu/accounts_menu.kv')
        Builder.load_file('AppMenus/Categories_menu/categories_menu.kv')
        Builder.load_file('MainScreen.kv')
        Builder.load_file('MyNavigationDrawer.kv')
        Builder.load_file('manager.kv')
        Builder.load_file('AppMenus/Categories_menu/categories_buttons_menu.kv')
        Builder.load_file('AppMenus/Transaction_menu/transaction_menu.kv')
        Builder.load_file('AppMenus/Accounts_menu/accounts_menu_debts.kv')

        return Manager()


if __name__ == '__main__':
    # makes empty data files
    create_savings_data_file('AppData/data_files/savings-data.txt')
    create_categories_data_file('AppData/data_files/categories-data.txt')
    create_accounts_data_file('AppData/data_files/accounts-data.txt')
    create_transaction_history_file('AppData/data_files/transaction-history.csv')

    # smartphone screen checking
    Window.size = (0.4 * 1080, 0.4 * 2280)

    # date
    date_today = datetime.date.today()

    current_year = date_today.year
    current_month = date_today.month
    current_day = date_today.day

    # current menu date
    days_in_month_icon_dict = {
        28: 'Icons/Month_days_icons/twenty-eight.png',
        29: 'Icons/Month_days_icons/twenty-nine.png',
        30: 'Icons/Month_days_icons/thirty.png',
        31: 'Icons/Month_days_icons/thirty-one.png'
    }

    current_menu_date = date_today

    current_menu_year = current_year
    current_menu_month = current_month

    days_in_current_menu_month = monthrange(current_menu_year, current_menu_month)[1]
    current_menu_month_name = month_name[current_menu_month]

    # start the app
    MoneyStatApp().run()
