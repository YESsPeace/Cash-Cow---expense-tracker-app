from kivy.properties import BooleanProperty, OptionProperty, StringProperty
from kivymd.uix.navigationdrawer import MDNavigationDrawer

from AppMenus.other_func import calculate


class balance_writer(MDNavigationDrawer):
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

    text_widget_id = StringProperty()

    default_sum_label_text = StringProperty('0')

    item_dict = StringProperty('account_info')
    item_dict_parameter = StringProperty('Balance')

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

    def done_pressed(self, *args):
        getattr(self.parent.ids, self.text_widget_id).text = self.ids.sum_label.text

        getattr(self.parent, self.item_dict)[self.item_dict_parameter] = self.ids.sum_label.text

        self.del_myself()

    def sign_btn_pressed(self, btn):
        if len(set(self.ids.sum_label.text).intersection({'+', '-', '÷', 'x'})):
            self.calculate_btn_pressed()
            self.ids.sum_label.text = self.ids.sum_label.text + btn.text

        elif self.ids.sum_label.text[-1] in ['+', '-', '÷', 'x']:
            self.ids.sum_label.text = self.ids.sum_label.text[:-1] + btn.text

        else:
            self.ids.sum_label.text = self.ids.sum_label.text + btn.text

        self.ids.done_btn.text = '='

    def calculate_btn_pressed(self):
        self.ids.sum_label.text = self.ids.sum_label.text.replace('x', '*')
        self.ids.sum_label.text = self.ids.sum_label.text.replace('÷', '/')
        self.ids.sum_label.text = str(eval(self.ids.sum_label.text))

    def del_myself(self):
        self.parent.remove_widget(self)
