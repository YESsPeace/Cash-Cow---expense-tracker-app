from typing import Union

from kivy.weakproxy import WeakProxy

from kivy.app import App
from kivy.metrics import dp
from kivy.properties import Clock
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDColorPicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

import config
from AppMenus.Accounts_menu.MenuForNewAccount.balance_writer import balance_writer
from AppMenus.Accounts_menu.MenuForNewAccount.menu_for_choice_new_account_type import menu_for_choice_new_account_type
from AppMenus.Categories_menu.Menu_For_new_category.icon_choice_menu import icon_choice_menu
from database import account_db_add, savings_db_add, savings_db_edit, accounts_db_edit, db_data_delete


class BoxLayoutButton(MDCard):
    radius = [0, 0, 0, 0]
    padding = [dp(5), dp(5), dp(5), dp(5)]
    md_bg_color = [0.12941176470588237, 0.12941176470588237, 0.12941176470588237, 1.0]


class menu_for_new_account(MDScreen):
    def __init__(self, *args, **kwargs):
        self.account_info = config.account_info.copy()

        print(*self.account_info.items(), sep='\n')

        super().__init__(*args, **kwargs)

        Clock.schedule_once(self.set_menu_widgets)

    def complete_pressed(self, *args):
        self.account_info['Name'] = self.ids.account_name_text_field.text

        self.account_info['Description'] = self.ids.account_description_text_field.text

        if self.account_info.get('new') is True:
            self.create_account()

        elif self.account_info != config.account_info:
            self.edit_account()

        else:
            self.quit_from_menu()
            Snackbar(text="There's nothing to change").open()

    def create_account(self, *args):
        print('# creation account started')

        if self.account_info['type'] == 'regular':
            account_db_add(self.account_info)

        elif self.account_info['type'] == 'savings':
            savings_db_add(self.account_info)

        self.quit_from_menu()
        Snackbar(text="Account created").open()

    def edit_account(self, *args):
        print('# editing account started')

        if self.account_info['type'] == 'regular':
            accounts_db_edit(self.account_info)

        elif self.account_info['type'] == 'savings':
            savings_db_edit(self.account_info)

        self.quit_from_menu()
        Snackbar(text="Account edited").open()

    def delete_account(self, *args):
        print('# deleting category started')

        db_data_delete(
            db_name='savings_db' if self.account_info['ID'].split('_')[0] == 'savings' else 'accounts_db',
            item_id=self.account_info['ID'],
        )

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

    def set_menu_widgets(self, *args):
        if self.account_info['type'] == 'savings':
            self.add_goal_button()

    def add_goal_button(self, *args):
        Goal_box = BoxLayoutButton(
            ripple_behavior=True,
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(50),
            on_release=lambda x: self.add_widget(
                balance_writer(
                    text_widget_id='goal_balance',
                    item_dict_parameter='Goal'
                )
            )
        )

        Goal_box.add_widget(
            MDScreen(
                MDLabel(
                    text='Goal'
                )
            ),
        )

        goal_balance_label = MDLabel(
            halign="right",
            text=str(self.account_info.setdefault('Goal', 0)),
            id='goal_balance'
        )

        Goal_box.add_widget(goal_balance_label)

        self.ids.buttons_box.add_widget(Goal_box, index=3)

        self.ids['goal_balance'] = WeakProxy(goal_balance_label)

    def change_account_type(self, *args):
        self.add_widget(
            menu_for_choice_new_account_type(
                new_account=False
            )
        )

    def switch_updated(self, switch, *args):
        if switch.active is True:
            self.account_info['IncludeInTheTotalBalance'] = 1

        else:
            self.account_info['IncludeInTheTotalBalance'] = 0

    def open_balance_writer(self, *args):
        self.add_widget(balance_writer(text_widget_id='account_balance'))

    def quit_from_menu(self, *args):
        self.parent.current = 'main'
        self.parent.remove_widget(self)
