from kivy.clock import Clock
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from AppData.data_scripts.GetData.GetDataFilesData import get_accounts_data, get_savings_data


class AccountsMenu_main(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.accounts_data_dict = get_accounts_data(
            accounts_data_file_path='AppData/data_files/accounts-data.txt'
        )
        self.savings_data_dict = get_savings_data(
            savings_data_file_path='AppData/data_files/savings-data.txt'
        )

        print("# accounts_data_dictionary:", self.accounts_data_dict)
        print('# savings_data_dictionary:', self.savings_data_dict)

        Clock.schedule_once(self.adding_accountsANDsavings_main_menu, 0)

    def adding_accountsANDsavings_main_menu(self, *args):
        accounts_amount, savings_amount = 0, 0

        for account_id in self.accounts_data_dict:
            my_widget = MDRectangleFlatIconButton(
                id=account_id, icon='Icons/Btn_icon/Accounts-icon-white.png',
                text=self.accounts_data_dict[account_id]['Name'],
                text_color='white',
                md_bg_color=self.accounts_data_dict[account_id]['Color'],
                size_hint=(1, 1), halign='left'
            )

            my_widget.add_widget(
                MDLabel(
                    text=self.accounts_data_dict[account_id]['Balance'] + ' ' +
                         self.accounts_data_dict[account_id]['Currency'],
                    halign='right'
                )
            )

            self.ids.accounts_Boxlines.add_widget(my_widget)
            if self.accounts_data_dict[account_id]['Currency'] == 'RUB':
                accounts_amount += float(self.accounts_data_dict[account_id]['Balance'])

        self.ids.accounts_amount.text = str(accounts_amount)

        for savings_id in self.savings_data_dict:
            my_widget = MDRectangleFlatIconButton(
                id=savings_id, icon='Icons/Btn_icon/Accounts-icon-white.png',
                text=self.savings_data_dict[savings_id]['Name'],
                text_color='white',
                md_bg_color=self.savings_data_dict[savings_id]['Color'],
                size_hint=(1, 1), halign='left'
            )

            my_widget.add_widget(
                MDLabel(
                    text=self.savings_data_dict[savings_id]['Balance'] + ' ' +
                         self.savings_data_dict[savings_id]['Currency'],
                    halign='right'
                )
            )

            self.ids.savings_Boxlines.add_widget(my_widget)

            if self.savings_data_dict[savings_id]['Currency'] == 'RUB':
                savings_amount += float(self.savings_data_dict[savings_id]['Balance'])

        self.ids.savings_amount.text = str(savings_amount)