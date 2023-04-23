from kivy.graphics import Color, Rectangle
from kivy.properties import Clock

import config
from AppMenus.BasicMenus import PopUpMenuBase, MenuForTransactionAddingBase


class MenuForTransactionAdding(PopUpMenuBase, MenuForTransactionAddingBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self.canvas.before:
            Color(0, 0, 0, .5)
            Rectangle(size=config.main_screen_size, pos=config.main_screen_pos)

        Clock.schedule_once(self.set_widgets_props)

    def set_widgets_props(self, *args):
        Clock.schedule_once(self.set_new_func_to_expense_and_incomes_buttons)
        Clock.schedule_once(self.set_new_func_to_transfer_buttons)

    def set_new_func_to_expense_and_incomes_buttons(self, *args):
        for menu_id, rv_id in [('Categories_buttons_menu', 'Categories_rv'),
                               ('Incomes_buttons_menu', 'Incomes_rv')]:

            new_data = getattr(self.ids, menu_id).get_rv_data()

            for item in new_data:
                item['on_release'] = self.on_button_callback(item['category_id'])

            getattr(getattr(self.ids, menu_id).ids, rv_id).data = new_data

    def set_new_func_to_transfer_buttons(self, *args):
        accounts_data = self.ids.AccountsMenu_main.get_accounts_data()

        for item in accounts_data:
            if item['viewclass'] == 'AccountsItem':
                item['on_release'] = self.on_button_callback(item['account_id'])

        self.ids.AccountsMenu_main.ids.accounts_rv.data = accounts_data

    def on_button_callback(self, widget_id):
        return lambda: self.open_menu_for_a_new_transaction(widget_id)

