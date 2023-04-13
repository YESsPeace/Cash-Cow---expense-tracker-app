from typing import Union

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.pickers import MDColorPicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

import config
from AppMenus.Categories_menu.Menu_For_new_category.icon_choice_menu import icon_choice_menu
from database import db_data_delete, db_data_edit, db_data_add


class BoxLayoutButton(MDCard, BoxLayout):
    pass


class menu_for_new_or_edit_category(MDScreen):
    def __init__(self, *args, **kwargs):
        self.currency = '₽'

        self.default_sum_label_text = f'{self.currency} 0'

        self.current_menu_date = config.current_menu_date

        self.category_item = config.category_item

        print(*self.category_item.items(), sep='\n')

        super().__init__(*args, **kwargs)

    def delete_category(self, *args):
        print('# deleting category started')
        db_data_delete(db_name='categories_db', item_id=self.category_item['ID'])
        self.del_myself()
        Snackbar(text="Category deleted").open()


    def complete_pressed(self, *args):
        if self.category_item.get('new') is True:
            self.create_category()

        elif (self.category_item != config.category_item) or \
                (self.ids.category_name_text_field.text != self.category_item['Name']):
            self.edit_category()

        else:
            self.del_myself()

    def create_category(self, *args):
        print('# creating category started')
        self.category_item['Name'] = self.ids.category_name_text_field.text

        db_data_add(
            db_name='categories_db',
            params=self.category_item
        )

        self.del_myself()
        Snackbar(text="Category created").open()

    def edit_category(self, *args):
        print('# editing category started')
        db_data_edit(
            db_name='categories_db',
            item_id=self.category_item['ID'],
            name=self.ids.category_name_text_field.text,
            icon=self.category_item['Icon'],
            color=self.category_item['Color']
        )

        self.del_myself()
        Snackbar(text="Category edited").open()

    def currency_pressed(self, *args) -> None:
        print('# currency button pressed')
        Snackbar(text="only in future.").open()

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

        self.ids.category_button.md_bg_color = selected_color[:-1] + [1]
        self.category_item['Color'] = selected_color[:-1] + [0.5]

    def open_icon_choice_menu(self, *args):
        self.add_widget(icon_choice_menu())

    def quit_from_menu(self, *args):
        self.parent.current = 'main'
        self.del_myself()

    def del_myself(self):
        self.parent.remove_widget(self)
