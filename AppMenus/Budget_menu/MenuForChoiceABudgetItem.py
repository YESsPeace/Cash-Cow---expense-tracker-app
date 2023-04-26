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

        Clock.schedule_once(self.set_widgets_props, -1)

    def set_widgets_props(self, *args):
        Clock.schedule_once(self.set_new_func_to_transfer_buttons)
        Clock.schedule_once(self.set_new_func_to_expense_and_incomes_buttons)

    def set_new_func_to_expense_and_incomes_buttons(self, *args):
        for menu_id, rv_id in [('Categories_buttons_menu', 'Categories_rv'),
                               ('Incomes_buttons_menu', 'Incomes_rv')]:

            new_data = getattr(self.ids, menu_id).get_rv_data()

            for item in new_data:
                if item['viewclass'] == 'CategoryItem':
                    item['on_release'] = self.on_button_callback(item['category_id'])

            getattr(getattr(self.ids, menu_id).ids, rv_id).data = new_data

    def set_new_func_to_transfer_buttons(self, *args):
        accounts_data = self.ids.AccountsMenu_main.get_accounts_data()

        for item in accounts_data:
            if item['viewclass'] == 'AccountsItem':
                if item['account_id'].split('_')[0] == 'account':
                    accounts_data.remove(item)
                    continue

                item['on_release'] = self.on_button_callback(item['account_id'])

        self.ids.AccountsMenu_main.ids.accounts_rv.data = accounts_data

    def on_button_callback(self, widget_id):
        return lambda: self.open_menu_for_edit_budget(widget_id)

    def open_menu_for_edit_budget(self, widget_id, *args):
        TopNotification(text='Editing and creating a budget will be in future versions').open()

        # app = App.get_running_app()
        #
        # app.root.ids.main.add_menu_for_edit_budget(widget_id)
