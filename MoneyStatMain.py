from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
import os

os.system('Data\TXT-categories-data.py')
os.system('Data\TXT-accounts.py')
os.system('Data\CSV-transaction-history.py')


def get_names_from_categories_data_txt():
    list_of_categories_name = []

    try:
        categories_data_file = open('Data/data_files/categories-data.txtf', 'r+', encoding="UTF8")

        for line in categories_data_file:
            list_of_categories_name.append(line.split('-')[1][:-1])

        categories_data_file.close()

        print('# list of categories name:', list_of_categories_name)

        return list_of_categories_name

    except FileNotFoundError:
        print("\033[36m{}".format('# [') + "\033[31m{}".format('ERROR') + "\033[36m{}".format('] ') +
              "\033[36m{}".format('[') + "\033[31m{}".format('DataFileNotFound') + "\033[36m{}".format('] ') +
              "\033[36m{}".format('categories_data.txt is not founded. Check if the TXT-categories-data.py is here'))

        return ['ERROR:'.rjust(16) + '\n' + 'File Is Not Founded'.rjust(16) for _ in range(12)]

class CategoriesMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.categories_list = get_names_from_categories_data_txt()

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

        self.ids.top_layout_background.height = dp(125 * 0.6)
    def return_page_layout(self):
        if not self.ids.my_PageLayout in self.ids.MainMenuWidget.children:

            self.ids.MainMenuWidget.remove_widget(self.ids.bottom_navigation_layout)

            self.ids.top_layout.add_widget(self.ids.middle_top_layout)
            self.ids.MainMenuWidget.add_widget(self.ids.my_PageLayout)
            self.ids.MainMenuWidget.add_widget(self.ids.bottom_navigation_layout)

            self.ids.top_layout_background.height = dp(125)

class MoneyStatApp(App):
    pass


if __name__ == '__main__':
    MoneyStatApp().run()
