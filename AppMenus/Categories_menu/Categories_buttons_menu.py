from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from AppData.data_scripts.GetData.GetDataFilesData import get_categories_data_from


class Categories_buttons_menu(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # getting data for categories
        self.categories_menu_button_data_dictionary = get_categories_data_from(
            categories_data_file_path='AppData/data_files/categories-data.txt'
        )
        print("# categories_menu_button_data_dictionary:", self.categories_menu_button_data_dictionary)

        Clock.schedule_once(self.button_data_setter, -1)

    def button_data_setter(self, *args):
        for button_id in self.categories_menu_button_data_dictionary:
            button = self.categories_menu_button_data_dictionary[button_id]

            box = MDBoxLayout(
                orientation='vertical',
                size_hint_y=None,
                md_bg_color=(.8, .6, .1, 1),
                height=dp(100)
            )

            box.add_widget(
                MDIconButton(
                    id=button_id,
                    text=button['Name'],
                    md_bg_color=button['Color'],
                    pos_hint={'center_x': .5},
                    icon_size="40sp",
                )
            )

            box.add_widget(
                MDLabel(
                    text=button['Name'],
                    size_hint=(1, .25),
                    halign='center',
                )
            )

            self.ids.GridCategoriesMenu.add_widget(box)
