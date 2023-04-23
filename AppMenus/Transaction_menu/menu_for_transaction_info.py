from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.properties import BooleanProperty, OptionProperty, NumericProperty, DictProperty
from kivymd.uix.navigationdrawer import MDNavigationDrawer

import config


class menu_for_transaction_info(MDNavigationDrawer):
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

    transaction_id = NumericProperty()

    transaction_data = DictProperty()

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self.canvas.before:
            Color(0, 0, 0, .5)
            Rectangle(size=config.main_screen_size, pos=config.main_screen_pos)

    def del_myself(self, *args):
        self.parent.remove_widget(self)

    def open_menu_for_edit_transaction(self, transaction_id, transaction_data):
        app = App.get_running_app()

        app.root.ids.main.open_menu_for_transaction_adding(transaction_id, transaction_data)
