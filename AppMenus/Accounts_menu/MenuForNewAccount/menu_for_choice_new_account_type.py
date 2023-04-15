from kivy.app import App
from kivy.properties import BooleanProperty, OptionProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.navigationdrawer import MDNavigationDrawer

import config


class BoxLayoutButton(MDCard, BoxLayout):
    pass


class menu_for_choice_new_account_type(MDNavigationDrawer):
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
        self.account_info = {
                'ID': None,
                'Name': '',
                'Color': [0.71, 0.72, 0.69, 0.5],
                'Icon': 'card',
                'new': True,
                'type': None
            }
        super().__init__(*args, **kwargs)

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

    def del_myself(self) -> None:
        self.parent.remove_widget(self)

    def open_menu_for_new_account(self, *args):
        config.account_info = self.account_info

        app = App.get_running_app()

        app.root.ids.main.add_menu_for_new_account()

        self.del_myself()