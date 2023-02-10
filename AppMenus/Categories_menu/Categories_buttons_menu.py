from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from random import choice

import config
from config import icon_list

from AppData.data_scripts.GetData.GetDataFilesData import get_categories_data_from


class WaterFill(Widget):
    def __init__(self, *args, **kwargs):
        self.level = config.level
        self.color = config.color
        super().__init__(*args, **kwargs)


class Categories_buttons_menu(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # getting data for categories
        self.categories_menu_button_data_dictionary = config.global_categories_data_dict

        print("# categories_menu_button_data_dictionary:", self.categories_menu_button_data_dictionary)

        Clock.schedule_once(self.button_data_setter, -1)

    def button_data_setter(self, *args):
        for button_id in self.categories_menu_button_data_dictionary:
            button = self.categories_menu_button_data_dictionary[button_id]

            config.level = choice([
                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1
            ])
            config.color = button['Color']

            print('Another', config.level)

            box = MDBoxLayout(
                orientation='vertical',
                size_hint_y=None,
                md_bg_color=(.23, .6, .5, 1),
                height=dp(100)
            )
            container = AnchorLayout()

            container.add_widget(WaterFill(
                pos_hint={'center_x': 0.5, 'top': 1},
                size=(dp(48), dp(48))
            ))

            container.add_widget(MDIconButton(
                pos_hint={'center_x': 0.5, 'top': 0.5},
                id=str(button_id),
                icon=choice(icon_list),
            ))

            box.add_widget(container)

            box.add_widget(
                MDLabel(
                    text=button['Name'],
                    size_hint=(1, .25),
                    halign='center',
                )
            )

            self.ids.GridCategoriesMenu.add_widget(box)
