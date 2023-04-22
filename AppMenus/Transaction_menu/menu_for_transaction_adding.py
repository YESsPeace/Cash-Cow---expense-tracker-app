from kivy.properties import OptionProperty, BooleanProperty, Clock
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

import config
from AppMenus.CashMenus.MenuForAnewTransaction import menu_for_a_new_transaction
from database import categories_db_read, accounts_db_read, savings_db_read, incomes_db_read


class MenuForTransactionAdding(MDNavigationDrawer):
    # the menu opening only in Transaction menu
    # it's needs for choosing what exactly will be in transaction
    # Account, Category of expense and other

    state = OptionProperty("open", options=("close", "open"))
    status = OptionProperty(
        "opened",
        options=(
            "closed",
            "opening_with_swipe",
            "opening_with_animation",
            "opened",
            "closing_with_swipe",
            "closing_with_animation",
        ),
    )
    enable_swiping = BooleanProperty(False)

    def update_status(self, *_) -> None:
        status = self.status
        if status == "closed":
            self.state = "close"
        elif status == "opened":
            self.state = "open"
        elif self.open_progress == 1 and status == "opening_with_animation":
            self.status = "opened"
            self.state = "open"
        elif self.open_progress == 0 and status == "closing_with_animation":
            self.status = "closed"
            self.state = "close"

            # when person start reselection first item, but close the menu not finish
            config.choosing_first_transaction = False

        elif status in (
                "opening_with_swipe",
                "opening_with_animation",
                "closing_with_swipe",
                "closing_with_animation",
        ):
            pass
        if self.status == "closed":
            self.opacity = 0
        else:
            self.opacity = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # getting data for expense
        self.expense_dict = categories_db_read() | incomes_db_read()
        # getting data for transfer
        self.transfer = accounts_db_read() | savings_db_read()

        Clock.schedule_once(self.set_widgets_props)

    def set_widgets_props(self, *args):
        if len(self.expense_dict) > 0 and len(self.transfer) > 0:
            Clock.schedule_once(self.set_new_func_to_expense_and_incomes_buttons)
            Clock.schedule_once(self.set_new_func_to_transfer_buttons)
        else:
            self.del_myself()
            Snackbar(text="Firstly create an account and an expense category").open()

    def set_new_func_to_expense_and_incomes_buttons(self, *args):
        for menu_id, rv_id in [('Categories_buttons_menu', 'Categories_rv'),
                                 ('Incomes_buttons_menu', 'Incomes_rv')]:

            new_data = getattr(self.ids, menu_id).get_rv_data()

            for item in new_data:
                item['on_release'] = self.on_account_callback(item['category_id'])

            getattr(getattr(self.ids, menu_id).ids, rv_id).data = new_data


    def set_new_func_to_transfer_buttons(self, *args):
        accounts_data = self.ids.AccountsMenu_main.get_accounts_data()

        for item in accounts_data:
            if item['viewclass'] == 'AccountsItem':
                item['on_release'] = self.on_account_callback(item['account_id'])

        self.ids.AccountsMenu_main.ids.accounts_rv.data = accounts_data

    def on_account_callback(self, widget_id):
        return lambda: self.put(widget_id)

    def on_category_callback(self, widget_id):
        return lambda _: self.put(widget_id)

    def del_myself(self, *args):
        self.parent.remove_widget(self)

    def put(self, widget_id, *args):
        # closing the old menu
        self.status = 'closed'

        # getting info for a new menu

        # reselection the first item
        if config.choosing_first_transaction:
            config.choosing_first_transaction = False
            if str(widget_id) in self.transfer:
                config.first_transaction_item = None
                config.first_transaction_item = {
                    'id': widget_id,
                    'Name': self.transfer[widget_id]['Name'],
                    'Color': self.transfer[widget_id]['Color'][:-1],
                    'Currency': 'RUB'  # last_transaction['FromCurrency']
                }
            else:
                Snackbar(text="You can't spend money from the category").open()



        # typical selection
        else:
            if len(config.history_dict) > 0:
                config.last_transaction_id = list(config.history_dict)[-1]
                last_transaction = config.history_dict[config.last_transaction_id]

                if last_transaction['Type'] in ['Transfer', 'Expenses']:
                    last_account = last_transaction['From']

                    if type(last_account) is tuple:
                        last_account = last_account[0]

                else:
                    last_account = last_transaction['To']

                    if type(last_account) is tuple:
                        last_account = last_account[0]

            else:
                last_account = 'account_1'

            config.first_transaction_item = {
                'id': last_account,
                'Name': self.transfer[last_account]['Name'],
                'Color': self.transfer[last_account]['Color'][:-1],
                'Currency': 'RUB'  # last_transaction['FromCurrency']
            }
            # second item
            config.second_transaction_item = (self.expense_dict | self.transfer)[widget_id]
            config.second_transaction_item['Color'] = config.second_transaction_item['Color'][:-1] + [1]
            config.second_transaction_item['id'] = widget_id

            if widget_id.split('_')[0] == 'income':
                config.first_transaction_item, config.second_transaction_item = config.second_transaction_item, config.first_transaction_item

            print(*config.second_transaction_item.items(), sep='\n')

            if str(widget_id) in self.transfer:
                config.second_transaction_item['Currency'] = self.transfer[str(widget_id)]['Currency']

            else:
                config.second_transaction_item['Currency'] = 'RUB'

        # checking
        # print('# first_transaction_item', config.first_transaction_item)
        # print('# second_transaction_item', config.second_transaction_item)

        # adding a new menu to the app
        self.parent.add_widget(menu_for_a_new_transaction())
        self.del_myself()
