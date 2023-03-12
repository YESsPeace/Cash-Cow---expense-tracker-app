from kivy.properties import NumericProperty, ListProperty
from kivy.uix.widget import Widget

import config


class WaterFill(Widget):
    level = NumericProperty(0)
    color = ListProperty([0.2, 0.2, 0.2, 1])