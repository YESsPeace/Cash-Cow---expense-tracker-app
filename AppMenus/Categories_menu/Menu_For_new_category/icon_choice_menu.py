from kivy.properties import BooleanProperty, OptionProperty
from kivymd.uix.button import MDIconButton
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.icon_definitions import md_icons
from kivy.clock import Clock

import config


class CustomIconItem(MDIconButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_release(self):
        self.parent.set_icon(icon_name=self.icon)


class icon_choice_menu(MDNavigationDrawer):
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

    def __init__(self, *args, **kwargs):
        self.category_item = config.category_item

        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.set_widget_props)

    def set_widget_props(self, *args):
        self.set_icons_grid()

    def set_icons_grid(self, *args):
        for icon_name in md_icons:
            color = [.55, .55, .55, 1]

            if icon_name == self.category_item.get('Icon'):
                color = [.9, .1, .1, 1]

            self.ids.rv.data.append(
                {
                    "viewclass": "MDIconButton",
                    "icon": icon_name,
                    "md_bg_color": color,
                    "on_release": lambda icon_name=icon_name: self.set_icon(icon_name),
                }
            )

    def set_icon(self, icon_name, *args):
        self.ids.icon_preview.icon = icon_name

    def complete_pressed(self, *args):
        self.parent.ids.category_button.icon = self.ids.icon_preview.icon
        print('# icon selected:', self.ids.icon_preview.icon)
        self.del_myself()

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

            self.del_myself()

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

    def del_myself(self):
        self.parent.remove_widget(self)
