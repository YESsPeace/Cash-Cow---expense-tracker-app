from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.progressbar import ProgressBar
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDRectangleFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

import config
from database import get_categories_month_data, budget_data_categories_read, \
    transaction_db_read, get_transaction_for_the_period


class BudgetMenu_in(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.current_spent = 0
        self.all_categories_spent = 0

        self.categories_month_data_dict = \
            get_categories_month_data(get_transaction_for_the_period(
                from_date=str(config.current_menu_date.replace(day=1)),
                to_date=str(config.current_menu_date.replace(day=config.days_in_current_menu_month)),
                history_dict=transaction_db_read()
            )
            )

        print('Categories_month_Budget_data_dict in BudgetMenu', *self.categories_month_data_dict.items(), sep='\n')

        self.categories_budget_data_dict = budget_data_categories_read()

        self.budget_data_date = str(config.current_menu_date)[:-3].replace('-', '')

        if self.budget_data_date in self.categories_budget_data_dict:
            print('Categories_Budget_data_dict in BudgetMenu',
                  *self.categories_budget_data_dict[self.budget_data_date].items(), sep='\n')

            Clock.schedule_once(self.set_categories_budget)

    def set_categories_budget(self, *args) -> None:
        for category_id in self.categories_budget_data_dict[self.budget_data_date]:
            if category_id in self.categories_month_data_dict:
                spent = int(self.categories_month_data_dict[category_id]['SUM'])

                self.current_spent += spent

                self.all_categories_spent += \
                    (spent / int(self.categories_budget_data_dict[self.budget_data_date][category_id]['Budgeted']))

            else:
                spent = 0

            progress = MDBoxLayout(
                MDBoxLayout(
                    MDLabel(
                        text=str(category_id) + ' ' +
                             str(config.global_categories_data_dict[category_id]['Name']),
                        halign='left'
                    ),
                    MDLabel(
                        text=str(self.categories_budget_data_dict[self.budget_data_date][category_id]['Currency']) +
                             ' ' + str(
                            self.categories_budget_data_dict[self.budget_data_date][category_id]['Budgeted']),
                        halign='right'
                    ),
                ),
                MDScreen(
                    ProgressBar(
                        max=int(self.categories_budget_data_dict[self.budget_data_date][category_id]['Budgeted']),
                        value=spent,
                    ),
                    size_hint_y=1.25
                ),
                MDBoxLayout(
                    MDLabel(
                        text='spent: ' + str(spent),
                        font_style='Caption',
                        halign='left',
                    ),
                    MDLabel(
                        text='budgeted: ' +
                             str(self.categories_budget_data_dict[self.budget_data_date][category_id]['Currency']) +
                             ' ' + str(
                            self.categories_budget_data_dict[self.budget_data_date][category_id]['Budgeted']),
                        font_style='Caption',
                        halign='right',
                    ),
                ),
                id=str(category_id) + '_budget',
                md_bg_color=(.45, .3, .1, 1),
                orientation='vertical',
                size_hint_y=None,
                height=dp(60),
                padding=dp(3)
            )

            self.ids.categories_budget.add_widget(progress)

        Clock.schedule_once(self.set_categories_list)
        Clock.schedule_once(self.calculate_n_set_categories_spent)

    def calculate_n_set_categories_spent(self, *args) -> None:
        print('All categories spent:',
              self.all_categories_spent / len(self.categories_budget_data_dict[self.budget_data_date]))
        self.ids.all_categories_ProgressBar.value = \
            (self.all_categories_spent / len(self.categories_budget_data_dict[self.budget_data_date])) * 100

        self.ids.spent_label.text = \
            str(sum([int(self.categories_month_data_dict[category_id]['SUM'])
                     for category_id in self.categories_month_data_dict
                     if category_id in self.categories_budget_data_dict[self.budget_data_date]]))

        self.ids.budgeted_label.text = \
            str(sum(
                [int(self.categories_budget_data_dict[self.budget_data_date][category_id]['Budgeted'])
                 for category_id in self.categories_budget_data_dict[self.budget_data_date]]
            ))

    def set_categories_list(self, *args) -> None:
        self.category_grid = MDGridLayout(
            MDAnchorLayout(
                MDRectangleFlatButton(
                    text='More',
                    size_hint_y=None,
                    height=dp(60),
                    md_bg_color=(.66, .66, .66, 1),
                    on_release=self.open_grid,
                )
            ),
            md_bg_color=(.3, .5, .4, 1),
            size_hint_y=None,
            adaptive_height=True,
            cols=4,
        )

        for category_id in config.global_categories_data_dict:
            if category_id in self.categories_budget_data_dict[self.budget_data_date]:
                continue

            category = config.global_categories_data_dict[category_id]

            self.category_grid.add_widget(
                MDBoxLayout(
                    MDIconButton(
                        pos_hint={'center_x': 0.5, 'top': 0.5},
                        id=str(category_id),
                        md_bg_color=category['Color'][:-1] + [1],
                        icon_size=dp(15),
                    ),
                    MDLabel(
                        text=category['Name'],
                        size_hint=(1, .25),
                        halign='center',
                    ),
                    orientation='vertical',
                    size_hint_y=None,
                    height=dp(60)
                ),
            )

        self.category_ScrollView = MDScrollView(
            self.category_grid,
            adaptive_height=True,
            size_hint=(1, None),
            height=dp(60),
        )

        self.ids.categories_budget.add_widget(self.category_ScrollView)

    def open_grid(self, widget) -> None:
        print('Open pressed')

        widget.parent.parent.parent.height = widget.parent.parent.height

        widget.parent.add_widget(
            MDRectangleFlatButton(
                text='Less',
                size_hint_y=None,
                height=dp(60),
                md_bg_color=(.66, .66, .66, 1),
                on_release=self.close_grid,
            )
        )

        widget.parent.remove_widget(widget)

    def close_grid(self, widget) -> None:
        print('Close pressed')

        widget.parent.parent.parent.height = dp(60)

        widget.parent.add_widget(
            MDRectangleFlatButton(
                text='More',
                size_hint_y=None,
                height=dp(60),
                md_bg_color=(.66, .66, .66, 1),
                on_release=self.open_grid,
            )
        )

        widget.parent.remove_widget(widget)