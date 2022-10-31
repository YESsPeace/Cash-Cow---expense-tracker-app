from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from warnings import warn
import os

os.system('Data\TXT-categories-data.py')
os.system('Data\TXT-accounts.py')
os.system('Data\CSV-transaction-history.py')


def get_names_from_categories_data_txt(path):
    return_list = []

    list_of_categories_name = []
    list_of_categories_color = []

    try:
        categories_data_file = open(path, 'r+', encoding="UTF8")

        for line in categories_data_file:
            list_of_categories_name.append(line.split('-')[1])
            list_of_categories_color.append(line.split('-')[2][:-1])

        categories_data_file.close()

        return_list.append(list_of_categories_name)
        return_list.append(list_of_categories_color)

        print('# list of categories name:', list_of_categories_name)
        print('# list of categories color:', list_of_categories_color)

        return return_list

    except FileNotFoundError:
        warn('categories_data.txt is not founded. Check if the TXT-categories-data.py is here', DataFileIsNotFounded)
        # warning message and return standard list
        return ['ERROR:'.rjust(16) + '\n' + 'File Is Not Founded'.rjust(16) for _ in range(12)]


class DataFileIsNotFounded(UserWarning):  # Warning message, my type
    pass


class MonthsMenu(BoxLayout):
    pass


class CategoriesMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.categories_list, self.categories_list_color = get_names_from_categories_data_txt(
            'Data/data_files/categories-data.txt')

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
