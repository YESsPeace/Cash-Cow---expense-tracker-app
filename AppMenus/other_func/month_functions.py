import datetime
from calendar import monthrange, month_name

import config


def load_previous_month(self, menu):
    config.current_menu_date = config.current_menu_date.replace(day=1)

    previous_month_date = config.current_menu_date - datetime.timedelta(days=1)

    load_month(self, previous_month_date, menu)

def load_next_month(self, menu):
    config.current_menu_date = config.current_menu_date.replace(day=int(config.days_in_current_menu_month))

    # getting next month
    next_month_date = config.current_menu_date + datetime.timedelta(days=1)

    load_month(self, next_month_date, menu)

def load_month(self, date, menu):
    # update data in python
    config.current_menu_date = date

    config.days_in_current_menu_month = monthrange(config.current_menu_date.year, config.current_menu_date.month)[1]
    config.current_menu_month_name = month_name[config.current_menu_date.month]

    # update data in menu
    self.ids.month_label.text = config.current_menu_month_name
    self.ids.month_icon.icon = config.days_in_month_icon_dict[config.days_in_current_menu_month]

    name_ = date.strftime("%Y") + '-' + date.strftime("%m")

    if not self.ids.my_swiper.has_screen(name_):
        self.ids.my_swiper.add_widget(menu(name=name_))


    self.ids.my_swiper.current = name_