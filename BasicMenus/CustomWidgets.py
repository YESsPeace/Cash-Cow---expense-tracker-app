from kivy.metrics import dp
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