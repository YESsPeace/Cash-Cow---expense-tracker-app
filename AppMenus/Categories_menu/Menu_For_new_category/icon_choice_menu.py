from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty
from kivymd.icon_definitions import md_icons
from kivymd.uix.card import MDCard

import config
from BasicMenus import PopUpMenuBase


class CustomIconItem(MDCard):
    radius = [0, 0, 0, 0]
    padding = [dp(5), dp(5), dp(5), dp(5)]
    spacing = dp(5)
    md_bg_color = [0.12941176470588237, 0.12941176470588237, 0.12941176470588237, 1.0]

    icon_name = StringProperty('android')
    color = ListProperty([0, 0, 0, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_release(self):
        self.parent.set_icon(icon_name=self.icon)


class icon_choice_menu(PopUpMenuBase):
    title_text = StringProperty('Category item')
    button_id = StringProperty('icon_button')
    info_dict_name = StringProperty('item')
    current_item_icon = StringProperty()

    def __init__(self, *args, **kwargs):
        self.category_item, self.account_item = config.category_item, config.account_info

        super().__init__(*args, **kwargs)

        with self.canvas.before:
            Color(0, 0, 0, .5)
            Rectangle(size=config.main_screen_size, pos=config.main_screen_pos)

        Clock.schedule_once(self.set_widget_props, 1)

    def set_widget_props(self, *args):
        self.set_icons_grid()

    def set_icons_grid(self, text="", search=False, *args):

        def add_icon_item(icon_name):
            self.ids.rv.data.append(
                {
                    "viewclass": "CustomIconItem",
                    "icon_name": icon_name,
                    "color": color,
                    "on_release": lambda icon_name=icon_name: self.set_icon(icon_name),
                }
            )

        self.ids.rv.data = []

        for icon_name in md_icons.keys():
            color = [.55, .55, .55, 1]

            if icon_name == self.current_item_icon:
                color = [.9, .1, .1, 1]

            if search:
                if text.lower() in icon_name.lower():
                    add_icon_item(icon_name)

            else:
                add_icon_item(icon_name)

    def set_icon(self, icon_name, *args):
        self.ids.icon_preview.icon = icon_name

    def complete_pressed(self, *args):
        getattr(self.parent.ids, self.button_id).icon = self.ids.icon_preview.icon
        print('# icon selected:', self.ids.icon_preview.icon)
        getattr(self.parent, self.info_dict_name)['Icon'] = self.ids.icon_preview.icon
        self.del_myself()
