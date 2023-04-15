from typing import Union

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.pickers import MDColorPicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

import config
from AppMenus.Categories_menu.Menu_For_new_category.icon_choice_menu import icon_choice_menu


class BoxLayoutButton(MDCard, BoxLayout):
    pass


class menu_for_new_account(MDScreen):
    def __init__(self, *args, **kwargs):
        self.account_info = config.account_info

        print(*self.account_info.items(), sep='\n')

        super().__init__(*args, **kwargs)

    def complete_pressed(self, *args):
        if self.account_info.get('new') is True:
            self.create_account()

        elif (self.account_info != config.account_info) or \
                (self.ids.category_name_text_field.text != self.account_info['Name']):
            self.edit_account()

        else:
            self.quit_from_menu()

    def create_account(self, *args):
        print('# creation account started')

        self.quit_from_menu()
        Snackbar(text="Account created").open()

    def edit_account(self, *args):
        print('# editing account started')

        self.quit_from_menu()
        Snackbar(text="Account edited").open()

    def delete_account(self, *args):
        print('# deleting category started')

        self.quit_from_menu()
        Snackbar(text="Account deleted").open()

    def open_icon_choice_menu(self, *args):
        self.add_widget(
            icon_choice_menu(
                title_text='Account icon',
                button_id='account_button',
                info_dict_name='account_info',
            )
        )

    def open_color_picker(self):
        self.color_picker = MDColorPicker(size_hint=(0.5, 0.85))
        self.color_picker.open()
        self.color_picker.bind(
            on_release=self.set_selected_color,
        )

    def set_selected_color(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        self.color_picker._real_remove_widget()
        print(f"Selected color is {selected_color}")
        print(type(selected_color))

        self.ids.account_button.md_bg_color = selected_color[:-1] + [1]
        self.account_info['Color'] = selected_color[:-1] + [0.5]

    def currency_pressed(self, *args) -> None:
        print('# currency button pressed')
        Snackbar(text="only in future.").open()

    def quit_from_menu(self, *args):
        self.parent.current = 'main'
        self.parent.remove_widget(self)
