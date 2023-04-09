from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

import config
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

    def complete_pressed(self, *args):
        if self.category_item.get('new') is True:
            self.create_category()

        else:
            self.edit_category_name()

    def create_category(self, *args):
        print('# creating category started')
        self.category_item['Name'] = self.ids.category_name_text_field.text

        db_data_add(
            db_name='categories_db',
            params=self.category_item
        )

    def edit_category_name(self, *args):
        print('# editing category started')
        db_data_edit(
            db_name='categories_db',
            item_id=self.category_item['ID'],
            name=self.ids.category_name_text_field.text,
        )

    def currency_pressed(self, *args):
        print('# currency button pressed')
        Snackbar(text="only in future.").open()

    def quit_from_menu(self, *args):
        self.parent.current = 'main'
        self.del_myself()

    def del_myself(self):
        self.parent.remove_widget(self)
