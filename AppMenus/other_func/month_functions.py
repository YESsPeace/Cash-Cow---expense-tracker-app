import datetime
from calendar import monthrange, month_name

from kivy.app import App
from kivy.uix.screenmanager import SlideTransition

import config


def load_previous_month(self, menu):
    config.current_menu_date = config.current_menu_date.replace(day=1)

    previous_month_date = config.current_menu_date - datetime.timedelta(days=1)

    self.ids.my_swiper.transition = SlideTransition(duration=.25, direction='right')
    load_month(self, previous_month_date, menu)


def load_next_month(self, menu):
    config.current_menu_date = config.current_menu_date.replace(day=int(config.days_in_current_menu_month))

    # getting next month
    next_month_date = config.current_menu_date + datetime.timedelta(days=1)

    self.ids.my_swiper.transition = SlideTransition(duration=.25, direction='left')
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

    if config.current_menu_date.strftime("%Y") + config.current_menu_date.strftime("%m") == \
            config.date_today.strftime("%Y") + config.date_today.strftime("%m"):
        self.ids.top_bar.md_bg_color = [.6, .1, .2, 1]


    else:
        self.ids.top_bar.md_bg_color = [.33, .33, .33, 1]


def update_menus(date_of_changes: str = None):
    app = App.get_running_app()

    app.root.ids.main.ids.AccountsMenu_id.ids.AccountsMenu_main_id.refresh_rv_data()

    if not date_of_changes is None:
        if '.' in date_of_changes:
            date_of_changes = date_of_changes.split('.')
            date_of_changes = f'{date_of_changes[-1]}-{date_of_changes[-2]}'

        else:
            date_of_changes = date_of_changes[:-3]

        for menu_id, swiper_id in [
            ('CategoriesMenu', 'my_swiper'),
            ('CategoriesMenu', 'incomes_swiper'),
            ('Transaction_menu', 'my_swiper'),
            ('BudgetMenu', 'my_swiper')
        ]:
            if getattr(getattr(app.root.ids.main.ids, menu_id).ids, swiper_id).has_screen(date_of_changes):
                getattr(getattr(app.root.ids.main.ids, menu_id).ids, swiper_id).get_screen(
                    date_of_changes).refresh_rv_data()


def update_total_balance_in_UI():
    app = App.get_running_app()

    for menu_id in ['AccountsMenu_id', 'CategoriesMenu', 'Transaction_menu', 'BudgetMenu']:
        getattr(app.root.ids.main.ids, menu_id).update_total_accounts_balance()
