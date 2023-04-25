from kivy.app import App
from kivy.properties import BooleanProperty, DictProperty
from kivy.uix.widget import Widget

from BasicMenus.CustomWidgets import TopNotification
from database import savings_db_read, incomes_db_read, accounts_db_read, categories_db_read, transaction_db_read


class MenuForTransactionAddingBase(Widget):
    choosing_first_transaction = BooleanProperty(False)
    choosing_second_transaction = BooleanProperty(True)

    first_transaction_item = DictProperty()
    second_transaction_item = DictProperty()

    def open_menu_for_a_new_transaction(self, widget_id, *args):
        accounts_data = accounts_db_read() | savings_db_read()
        categories_data = categories_db_read() | incomes_db_read()
        history_dict = transaction_db_read()

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
                TopNotification(text="You can't spend money from the category").open()
                return

        # typical selection
        else:
            if len(history_dict) > 0:
                last_transaction_id = list(history_dict)[-1]
                last_transaction = history_dict[last_transaction_id]

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

        if first_transaction_item['id'] == second_transaction_item['id']:
            TopNotification(text="You are trying to write an operation " + \
                                 f"from {first_transaction_item['Name']} to " + \
                                 f"{second_transaction_item['Name']}").open()
            return

        app = App.get_running_app()

        app.root.ids.main.add_menu_for_a_new_transaction(
            first_transaction_item=first_transaction_item,
            second_transaction_item=second_transaction_item
        )

        if hasattr(self, 'del_myself'):
            self.del_myself()

        elif hasattr(self.parent.parent.parent, 'del_myself'):
            self.parent.parent.parent.del_myself()
