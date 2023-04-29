import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color

import config
from BasicMenus import PopUpMenuBase, MenuForTransactionAddingBase
from BasicMenus.CustomWidgets import TopNotification


class MenuForChoiceABudgetItem(PopUpMenuBase, MenuForTransactionAddingBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self.canvas.before:
            Color(0, 0, 0, .5)
            Rectangle(size=config.main_screen_size, pos=config.main_screen_pos)

        threading.Thread(target=self.set_widgets_props).start()

    def set_widgets_props(self, *args):
        Clock.schedule_once(self.set_new_func_to_expense_and_incomes_buttons, 1)
        Clock.schedule_once(self.set_new_func_to_transfer_buttons, 1)

    def set_new_func_to_expense_and_incomes_buttons(self, *args):
        for menu_id, rv_id in [('Categories_buttons_menu', 'Categories_rv'),
                               ('Incomes_buttons_menu', 'Incomes_rv')]:
            threading.Thread(target=getattr(self.ids, menu_id).refresh_rv_data, args=(self.on_button_callback,)).start()

    def set_new_func_to_transfer_buttons(self, *args):
        accounts_data = self.ids.AccountsMenu_main.get_accounts_data()
        new_data = []

        for item in accounts_data:
            if item['viewclass'] == 'AccountsItem':
                if item['account_id'].split('_')[0] == 'savings':
                    item['on_release'] = self.on_button_callback(item['account_id'])
                    new_data.append(item)

        Clock.schedule_once(lambda dt: self.ids.AccountsMenu_main.ids.accounts_rv.data.clear())
        Clock.schedule_once(lambda dt: setattr(self.ids.AccountsMenu_main.ids.accounts_rv, 'data', new_data))

    def on_button_callback(self, widget_id):
        return lambda: self.open_menu_for_edit_budget(widget_id)

    def open_menu_for_edit_budget(self, widget_id, *args):
        TopNotification(text='Editing and creating a budget will be in future versions').open()

        # app = App.get_running_app()
        #
        # app.root.ids.main.add_menu_for_edit_budget(widget_id)
