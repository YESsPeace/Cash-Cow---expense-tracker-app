from kivy.uix.widget import Widget

import config


class WaterFill(Widget):
    def __init__(self, *args, **kwargs):
        self.level = config.level
        self.color = config.color
        super().__init__(*args, **kwargs)