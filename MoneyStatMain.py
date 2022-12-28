import datetime
from calendar import monthrange, month_name

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import Clock, ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

from AppData.data_scripts.Creating_data_files.CsvTransactionHistory import create_transaction_history_file
from AppData.data_scripts.Creating_data_files.TxtAccountsData import create_accounts_data_file
from AppData.data_scripts.Creating_data_files.TxtCategoriesData import create_categories_data_file
from AppData.data_scripts.Creating_data_files.TxtSavingsData import create_savings_data_file
from AppData.data_scripts.GetData.GetDataFilesData import get_accounts_data, get_categories_data_from, get_savings_data
from AppData.data_scripts.GetData.GetHistoryDataForThePeriod import get_transaction_history, \
    get_transaction_for_the_period


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

        Clock.schedule_once(self.adding_accountsANDsavings_main_menu, 0)

    def adding_accountsANDsavings_main_menu(self, *args):
        accounts_amount, savings_amount = 0, 0

        for account_id in self.accounts_data_dict:
            my_widget = MDRectangleFlatIconButton(
                id=account_id, icon='Icons/Btn_icon/Accounts-icon-white.png',
                text=self.accounts_data_dict[account_id]['Name'],
                text_color='white',
                md_bg_color=self.accounts_data_dict[account_id]['Color'],
                size_hint=(1, 1), halign='left'
            )

            my_widget.add_widget(
                MDLabel(
                    text=self.accounts_data_dict[account_id]['Balance'] + ' ' +
                         self.accounts_data_dict[account_id]['Currency'],
                    halign='right'
                )
            )

            self.ids.accounts_Boxlines.add_widget(my_widget)
            if self.accounts_data_dict[account_id]['Currency'] == 'RUB':
                accounts_amount += float(self.accounts_data_dict[account_id]['Balance'])

        self.ids.accounts_amount.text = str(accounts_amount)

        for savings_id in self.savings_data_dict:
            my_widget = MDRectangleFlatIconButton(
                id=savings_id, icon='Icons/Btn_icon/Accounts-icon-white.png',
                text=self.savings_data_dict[savings_id]['Name'],
                text_color='white',
                md_bg_color=self.savings_data_dict[savings_id]['Color'],
                size_hint=(1, 1), halign='left'
            )

            my_widget.add_widget(
                MDLabel(
                    text=self.savings_data_dict[savings_id]['Balance'] + ' ' +
                         self.savings_data_dict[savings_id]['Currency'],
                    halign='right'
                )
            )

            self.ids.savings_Boxlines.add_widget(my_widget)

            if self.savings_data_dict[savings_id]['Currency'] == 'RUB':
                savings_amount += float(self.savings_data_dict[savings_id]['Balance'])

        self.ids.savings_amount.text = str(savings_amount)


class AccountsMenu_debts(MDScreen):
    pass


class AccountsMenu_stat(MDScreen):
    def click(self):
        self.remove_widget(self.ids.AccountsMenu_stat_label)


class CategoriesMenu(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        # just for first creating widgets
        self.current_menu_date = str(current_menu_date)[:-3]
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

        if (self.ids.my_swiper.index == 0) or self.ids.my_swiper.previous_slide.name != last_month_date.strftime("%Y") + \
                '-' + last_month_date.strftime("%m"):
            self.ids.my_swiper.add_widget(Categories_buttons_menu(name=last_month_date.strftime("%Y") + '-' +
                                                                       last_month_date.strftime("%m")), index=-1)
            # current_menu_month_name
            # self.ids.my_swiper.index = 1
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

        if (self.ids.my_swiper.index == len(self.ids.my_swiper.slides) - 1) or \
                self.ids.my_swiper.next_slide.name != next_month_date.strftime("%Y") + \
                '-' + next_month_date.strftime("%m"):
            self.ids.my_swiper.add_widget(Categories_buttons_menu(name=next_month_date.strftime("%Y") + '-' +
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

        Clock.schedule_once(self.button_data_setter, 0)

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
    def __init__(self, *args, **kwargs):
        super(Transaction_menu, self).__init__(**kwargs)

        # getting actually data for menu settings and meny title
        self.current_menu_date = str(current_menu_date)[:-3]
        self.current_menu_month_name = current_menu_month_name
        self.days_in_month_icon_dict = days_in_month_icon_dict
        self.days_in_current_menu_month = days_in_current_menu_month

        # getting history data
        Transaction_menu.history_dict = get_transaction_history(
            history_file_path='AppData/data_files/transaction-history.csv',
            categories_data_file_path='AppData/data_files/categories-data.txt',
            accounts_data_file_path='AppData/data_files/accounts-data.txt'
        )

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

        if (self.ids.my_swiper.index == 0) or self.ids.my_swiper.previous_slide.name != \
                last_month_date.strftime("%Y") + '-' + last_month_date.strftime("%m"):
            self.ids.my_swiper.add_widget(Transaction_menu_in(name=last_month_date.strftime("%Y") + '-' +
                                                                   last_month_date.strftime("%m")), index=-1)
            # current_menu_month_name
            # self.ids.my_swiper.index = 1
            print('After-previous', self.ids.my_swiper.slides)

        self.ids.my_swiper.index = self.ids.my_swiper.index - 1

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

        if (self.ids.my_swiper.index == len(self.ids.my_swiper.slides) - 1) or \
                self.ids.my_swiper.next_slide.name != next_month_date.strftime("%Y") + \
                '-' + next_month_date.strftime("%m"):
            self.ids.my_swiper.add_widget(Transaction_menu_in(name=next_month_date.strftime("%Y") + '-' +
                                                                   next_month_date.strftime("%m")))
            # current_menu_month_name
            print('After-next', self.ids.my_swiper.slides)

        self.ids.my_swiper.index = self.ids.my_swiper.index + 1

        # self.ids.my_swiper.load_next()


class Transaction_menu_in(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # setting local variable for history dictionary from main Transaction menu
        self.history_dict = Transaction_menu.history_dict
        print(*self.history_dict.items(), sep='\n')

        print(str(current_menu_date.replace(day=1)))
        print(str(current_menu_date))

        Clock.schedule_once(self.history_setter, 0)

    def history_setter(self, *args):
        global current_menu_date, current_menu_month_name

        # the period is current menu month
        # it's from first day of the month to now
        print(*get_transaction_for_the_period(
            from_date=str(current_menu_date.replace(day=1)),
            to_date=str(current_menu_date),
            history_dict=self.history_dict
        ).items(), sep='\n')

class MainSrceen(MDScreen):
    def current_menu_month_name(self):
        return current_menu_month_name

    def set_transaction_menu_in(self):
        self.ids.Transaction_menu.ids.my_swiper.add_widget(Transaction_menu_in(name=str(current_menu_date)[:-3]))

    def set_categories_menu_buttons(self):
        self.ids.CategoriesMenu.ids.my_swiper.add_widget(Categories_buttons_menu(name=str(current_menu_date)[:-3]))

    def del_widgets_with_month(self):
        self.ids.CategoriesMenu.ids.my_swiper.clear_widgets()
        self.ids.Transaction_menu.ids.my_swiper.clear_widgets()


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
        Builder.load_file('AppMenus/Transaction_menu/transaction_menu_in.kv')

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
