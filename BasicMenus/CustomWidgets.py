from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import Snackbar


class BoxLayoutButton(MDCard):
    radius = [0, 0, 0, 0]
    padding = [dp(5), dp(5), dp(5), dp(5)]
    ripple_behavior = True


class TopNotification(Snackbar):
    snackbar_animation_dir = 'Top'
    duration = 2
    font_size = '16sp'


class ErrorNotification(Snackbar):
    auto_dismiss = False
    font_size = '16sp'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_once(self.set_buttons)

    def set_buttons(self, *args):
        self.buttons = [
            MDFlatButton(
                text="OK",
                text_color=(1, 1, 1, 1),
                on_release=self.dismiss
            )
        ]
