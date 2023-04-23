from kivy.app import App
from kivy.properties import BooleanProperty, OptionProperty, DictProperty
from kivy.uix.widget import Widget
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.snackbar import Snackbar

import config
from database import accounts_db_read, savings_db_read, categories_db_read, incomes_db_read


class MenuForTransactionAddingBase(Widget):
    choosing_first_transaction = BooleanProperty(False)
    choosing_second_transaction = BooleanProperty(True)

    first_transaction_item = DictProperty()
    second_transaction_item = DictProperty()

    def open_menu_for_a_new_transaction(self, widget_id, *args):

        accounts_data = accounts_db_read() | savings_db_read()
        categories_data = categories_db_read() | incomes_db_read()

        # reselection the first item
        if self.choosing_first_transaction:
            if str(widget_id) in accounts_data:
                first_transaction_item = {
                    'id': widget_id,
                    'Name': accounts_data[widget_id]['Name'],
                    'Color': accounts_data[widget_id]['Color'][:-1],
                    'Currency': 'RUB'  # last_transaction['FromCurrency']
                }

                second_transaction_item = self.second_transaction_item

            else:
                Snackbar(text="You can't spend money from the category").open()
                return

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

            first_transaction_item = {
                'id': last_account,
                'Name': accounts_data[last_account]['Name'],
                'Color': accounts_data[last_account]['Color'][:-1],
                'Currency': 'RUB'  # last_transaction['FromCurrency']
            }
            # second item
            second_transaction_item = (categories_data | accounts_data)[widget_id]
            second_transaction_item['Color'] = second_transaction_item['Color'][:-1] + [1]
            second_transaction_item['id'] = widget_id

            if widget_id.split('_')[0] == 'income':
                first_transaction_item, second_transaction_item = second_transaction_item, first_transaction_item

            if str(widget_id) in accounts_data:
                second_transaction_item['Currency'] = accounts_data[str(widget_id)]['Currency']

            else:
                second_transaction_item['Currency'] = 'RUB'

        # print('# first_transaction_item', first_transaction_item)
        # print('# second_transaction_item', second_transaction_item)

        app = App.get_running_app()

        app.root.ids.main.add_menu_for_a_new_transaction(
                first_transaction_item=first_transaction_item,
                second_transaction_item=second_transaction_item
            )

        if hasattr(self, 'del_myself'):
            self.del_myself()


class PopUpMenuBase(MDNavigationDrawer):
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

    def del_myself(self, *args):
        self.parent.remove_widget(self)
