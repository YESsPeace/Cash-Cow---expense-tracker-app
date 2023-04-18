from kivy.properties import OptionProperty, BooleanProperty, Clock
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.screen import MDScreen

import config
from AppMenus.CashMenus.MenuForAnewTransaction import menu_for_a_new_transaction
from database import categories_db_read, accounts_db_read, savings_db_read


class MenuForTransactionAdding(MDNavigationDrawer):
    # the menu opening only in Transaction menu
    # it's needs for choosing what exactly will be in transaction
    # Account, Category of expense and other

    state = OptionProperty("open", options=("close", "open"))
    status = OptionProperty(
        "closed",
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
        self.expense_dict = categories_db_read()

        # getting data for transfer
        self.transfer = accounts_db_read() | savings_db_read()

        # adding button to expense tab
        Clock.schedule_once(self.adding_buttons_to_expense_tab)

    def adding_buttons_to_expense_tab(self, *args):
        Clock.schedule_once(self.get_new_func_to_transfer_buttons)

        for button_id in self.expense_dict:
            box = MDScreen(
                md_bg_color=(.8, .3, .4, 1)
            )

            anchor_btn = MDAnchorLayout(md_bg_color=(.3, .6, .4, 1))
            anchor_btn.add_widget(
                MDIconButton(
                    id=str(button_id),
                    text=self.expense_dict[button_id]['Name'],
                    md_bg_color=list(self.expense_dict[button_id]['Color'][:-1]) + [1],
                    icon_size="32sp",
                    on_release=self.put
                )
            )
            box.add_widget(anchor_btn)

            box.add_widget(
                MDLabel(
                    text=self.expense_dict[button_id]['Name'],
                    pos_hint={'center_x': .5, 'top': 1},
                    size_hint=(1, .25),
                    halign='center',
                )
            )

            self.ids.expense_layout.add_widget(box)

    def adding_buttons_to_transfer_tab(self, *args):
        for account in self.transfer.values():
            box = MDScreen(
                md_bg_color=(.8, .3, .4, 1)
            )

            anchor_btn = MDAnchorLayout(md_bg_color=(.3, .6, .4, 1))
            anchor_btn.add_widget(
                MDIconButton(
                    md_bg_color=account['Color'],
                    icon_size="32sp"
                )
            )
            box.add_widget(anchor_btn)

            box.add_widget(
                MDLabel(
                    text=account['Name'],
                    pos_hint={'center_x': .5, 'top': 1},
                    size_hint=(1, .25),
                    halign='center',
                )
            )

            self.ids.transfer_layout.add_widget(box)

    def get_new_func_to_transfer_buttons(self, *args):
        for button in self.ids.AccountsMenu_main.ids.accounts_Boxlines.children:
            button.bind(on_press=self.put)

        for button in self.ids.AccountsMenu_main.ids.savings_Boxlines.children:
            button.bind(on_press=self.put)

    def put(self, widget, **kwargs):
        # closing the old menu
        self.status = 'closed'

        # getting info for a new menu

        # reselection the first item
        if config.choosing_first_transaction:
            if str(widget.id) in self.transfer:
                config.first_transaction_item = {'id': widget.id, 'Name': widget.text, 'Color': widget.md_bg_color,
                                                 'Currency': self.transfer[str(widget.id)]['Currency']}

            config.choosing_first_transaction = False

        # typical selection
        else:
            # first_item
            config.last_transaction_id = list(config.history_dict)[-1]

            last_id = -1
            while not config.history_dict[config.last_transaction_id]['Type'] in ['Transfer', 'Expenses']:
                last_id -= 1
                config.last_transaction_id = list(config.history_dict)[last_id]

            last_transaction = config.history_dict[config.last_transaction_id]

            last_account = last_transaction['From']

            config.first_transaction_item = {'id': last_account,
                                             'Name':
                                                 config.global_accounts_data_dict[last_account]['Name'],
                                             'Color': config.global_accounts_data_dict[last_account]['Color'],
                                             'Currency': last_transaction['FromCurrency']
                                             }
            # second item
            config.second_transaction_item = {'id': widget.id, 'Name': widget.text, 'Color': widget.md_bg_color}

            print(*config.second_transaction_item.items(), sep='\n')

            if str(widget.id) in self.transfer:
                config.second_transaction_item['Currency'] = self.transfer[str(widget.id)]['Currency']

            else:
                config.second_transaction_item['Currency'] = 'RUB'

        # checking
        # print('# first_transaction_item', config.first_transaction_item)
        # print('# second_transaction_item', config.second_transaction_item)

        # adding a new menu to the app
        self.parent.add_widget(menu_for_a_new_transaction())