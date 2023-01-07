from kivymd.uix.boxlayout import MDBoxLayout

import config


class date_label_for_transaction_history_menu(MDBoxLayout):

    def __init__(self, *args, **kwargs):
        self.date = config.Transaction_menu_in_last_date
        super().__init__(*args, **kwargs)
