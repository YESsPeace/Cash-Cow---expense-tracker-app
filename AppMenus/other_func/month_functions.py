import datetime
from calendar import monthrange, month_name

from kivy.app import App

import config
from AppMenus.Budget_menu.BudgetMenu_in import BudgetMenu_in


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


def update_month_menu_by_date(self, date_of_changes: str, main_menu_id: str, month_menu_name):
    date_of_changes = str(date_of_changes)

    if '.' in date_of_changes:
        date_of_changes = date_of_changes.split('.')
        date_of_changes = f'{date_of_changes[-1]}-{date_of_changes[-2]}'

    else:
        date_of_changes = date_of_changes[:-3]

    if getattr(self.parent.ids, main_menu_id).ids.my_swiper.has_screen(date_of_changes):
        getattr(self.parent.ids, main_menu_id).ids.my_swiper.remove_widget(
            getattr(self.parent.ids, main_menu_id).ids.my_swiper.get_screen(date_of_changes)
        )

        # # new temp_date values
        # temp_date = config.current_menu_date
        # temp_menu_month_name = config.current_menu_month_name
        # temp_days_in_current_menu_month = config.days_in_current_menu_month
        #
        # # replace date_value for create a new screen of Transaction_menu
        # config.current_menu_date = config.current_menu_date.replace(
        #     day=int(self.date_.split('.')[0]),
        #     month=int(self.date_.split('.')[1]),
        #     year=int(self.date_.split('.')[2])
        # )

        # config.current_menu_month_name = month_name[config.current_menu_date.month]
        # config.days_in_current_menu_month = monthrange(config.current_menu_date.year,
        #                                                config.current_menu_date.month)[1]

        # add a new screen of main_menu
        if month_menu_name == 'BudgetMenu_in':
            getattr(self.parent.ids, main_menu_id).ids.my_swiper.add_widget(
                BudgetMenu_in(name=date_of_changes)
            )

        # # restore old date values
        # config.current_menu_date = temp_date
        # config.current_menu_month_name = temp_menu_month_name
        # config.days_in_current_menu_month = temp_days_in_current_menu_month


def update_total_balance_in_UI():
    app = App.get_running_app()

    for menu_id in ['AccountsMenu_id', 'CategoriesMenu', 'Transaction_menu', 'BudgetMenu']:
        getattr(app.root.ids.main.ids, menu_id).update_total_accounts_balance()
