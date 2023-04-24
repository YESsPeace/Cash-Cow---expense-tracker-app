from typing import Union
from functools import cache

from kivy.metrics import dp
from kivymd.uix.pickers import MDColorPicker
from kivymd.uix.screen import MDScreen


class MenuForEditItemBase(MDScreen):
    @cache
    def open_color_picker(self):
        self.color_picker = MDColorPicker(size_hint=(None, None), size=(dp(350), dp(600)))
        self.color_picker.open()
        self.color_picker.bind(
            on_release=self.set_selected_color,
        )

    def set_selected_color(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        self.color_picker._real_remove_widget()
        print(f"Selected color is {selected_color}")
        print(type(selected_color))

        self.ids.icon_button.md_bg_color = selected_color[:-1] + [1]
        self.item['Color'] = selected_color[:-1] + [0.5]

    def quit_from_menu(self, *args):
        self.parent.current = 'main'
        self.del_myself()

    def del_myself(self):
        self.parent.remove_widget(self)
