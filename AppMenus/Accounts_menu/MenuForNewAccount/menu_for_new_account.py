from kivy.metrics import dp
from kivy.properties import Clock
from kivy.weakproxy import WeakProxy
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

import config
from AppMenus.Accounts_menu.MenuForNewAccount.balance_writer import balance_writer
from AppMenus.Accounts_menu.MenuForNewAccount.menu_for_choice_new_account_type import menu_for_choice_new_account_type
from AppMenus.Categories_menu.Menu_For_new_category.icon_choice_menu import icon_choice_menu
from AppMenus.other_func import update_total_balance_in_UI, update_menus
from BasicMenus import MenuForEditItemBase
from BasicMenus.CustomWidgets import TopNotification
from database import account_db_add, savings_db_add, savings_db_edit, accounts_db_edit, db_data_delete


class BoxLayoutButton(MDCard):
    radius = [0, 0, 0, 0]
    padding = [dp(5), dp(5), dp(5), dp(5)]
    ripple_behavior = True


class menu_for_new_account(MenuForEditItemBase):
    def __init__(self, *args, **kwargs):
        self.item = config.account_info.copy()

        print(*self.item.items(), sep='\n')

        super().__init__(*args, **kwargs)

        Clock.schedule_once(self.set_menu_widgets, -1)

    def complete_pressed(self, *args):
        self.item['Name'] = self.ids.account_name_text_field.text

        self.item['Description'] = self.ids.account_description_text_field.text

        if self.item.get('new') is True:
            self.create_account()

        elif self.item != config.account_info:
            self.edit_account()

        else:
            self.quit_from_menu()
            TopNotification(text="There's nothing to change").open()

    def create_account(self, *args):
        print('# creation account started')

        if self.item['type'] == 'regular':
            account_db_add(self.item)

        elif self.item['type'] == 'savings':
            savings_db_add(self.item)

        update_total_balance_in_UI()
        update_menus(str(config.current_menu_date))
        self.quit_from_menu()
        TopNotification(text="Account created").open()


    def edit_account(self, *args):
        print('# editing account started')

        if self.item['type'] == 'regular':
            accounts_db_edit(self.item)

        elif self.item['type'] == 'savings':
            savings_db_edit(self.item)

        update_total_balance_in_UI()
        update_menus(str(config.current_menu_date))
        self.quit_from_menu()
        TopNotification(text="Account edited").open()


    def delete_account(self, *args):
        print('# deleting category started')

        if self.item['new'] is True:
            TopNotification(text="Account not yet created to be deleted").open()
            return

        db_data_delete(
            db_name='savings_db' if self.item['ID'].split('_')[0] == 'savings' else 'accounts_db',
            item_id=self.item['ID'],
        )

        update_total_balance_in_UI()
        update_menus(str(config.current_menu_date))
        self.quit_from_menu()
        TopNotification(text="Account deleted").open()

    def open_icon_choice_menu(self, *args):
        self.add_widget(
            icon_choice_menu(
                title_text='Account icon',
            )
        )

    def currency_pressed(self, *args) -> None:
        print('# currency button pressed')
        TopNotification(text="only in future.").open()

    def set_menu_widgets(self, *args):
        if self.item['type'] == 'savings':
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
            text=str(self.item.setdefault('Goal', 0)),
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
            self.item['IncludeInTheTotalBalance'] = 1

        else:
            self.item['IncludeInTheTotalBalance'] = 0

    def open_balance_writer(self, *args):
        self.add_widget(balance_writer(text_widget_id='account_balance'))
