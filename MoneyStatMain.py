from kivy.app import App
from kivy.metrics import dp
from kivy.properties import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from warnings import warn
import os

from MyWarningMessages import DataFileIsNotFounded

os.system('Data\TXT-categories-data.py')
os.system('Data\TXT-accounts.py')
os.system('Data\CSV-transaction-history.py')


class MonthsMenu(BoxLayout):
    pass


def categories_menu_buttons_data(path):
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
        warn('categories_data.txt is not founded. Check if the TXT-categories-data.py is here',
             DataFileIsNotFounded)
        # warning message and return standard list
        return ['ERROR:'.rjust(16) + '\n' + 'File Is Not Founded'.rjust(16) for _ in range(12)]


class CategoriesMenu(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        self.categories_menu_button_data_dictionary = categories_menu_buttons_data(
            'Data/data_files/categories-data.txt')
        print("# categories_menu_button_data_dictionary:", self.categories_menu_button_data_dictionary)

        Clock.schedule_once(self.button_data_setter)

    def button_data_setter(self, *args):
        for button_id in self.ids:
            getattr(self.ids, button_id).text = self.categories_menu_button_data_dictionary[button_id]['Name']
            getattr(self.ids, button_id).background_color = self.categories_menu_button_data_dictionary[button_id][
                'Color']


class MainMenuWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # buttons I want to set
        self.toggle_button1 = ToggleButton(text='ACCOUNTS', group='sex', state='down', allow_no_selection=False)
        self.toggle_button2 = ToggleButton(text='', group='sex', size_hint=(None, 1), width=dp(50),
                                           allow_no_selection=False, background_normal='Icons/statistica.png',
                                           background_down='Icons/statistica_down.png')

    def change_the_middle_top_layout(self):
        # removing widgets which were before
        self.ids.middle_top_layout.remove_widget(self.ids.left_btn)
        self.ids.middle_top_layout.remove_widget(self.ids.middle_btn)
        self.ids.middle_top_layout.remove_widget(self.ids.right_btn)
        # adding the new toggle buttons
        self.ids.middle_top_layout.add_widget(self.toggle_button1)
        self.ids.middle_top_layout.add_widget(self.toggle_button2)

    def remove_the_changes_of_the_middle_top_layout(self):
        if self.toggle_button1 in list(self.ids.middle_top_layout.children):
            # removing the toggle buttons
            self.ids.middle_top_layout.remove_widget(self.toggle_button1)
            self.ids.middle_top_layout.remove_widget(self.toggle_button2)
            # adding the old buttons
            self.ids.middle_top_layout.add_widget(self.ids.left_btn)
            self.ids.middle_top_layout.add_widget(self.ids.middle_btn)
            self.ids.middle_top_layout.add_widget(self.ids.right_btn)

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
