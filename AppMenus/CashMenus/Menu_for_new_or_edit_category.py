from kivy.clock import Clock
from kivymd.uix.screen import MDScreen

import config


class menu_for_new_or_edit_category(MDScreen):

    def __init__(self, *args, **kwargs):
        self.currency = '₽'

        self.default_sum_label_text = f'{self.currency} 0'

        self.current_menu_date = config.current_menu_date

        self.category_item = config.category_item

        print(*self.category_item.items(), sep='\n')

        super().__init__(*args, **kwargs)

        Clock.schedule_once(self.set_widgets_prop)

    def quit_from_menu(self):
        self.parent.current = 'main'
        self.del_myself()

    def del_myself(self):
        self.parent.remove_widget(self)

    def set_widgets_prop(self, *args):
        pass

    def write_category_into_db(self, budgeted_sum, *args):
        pass
