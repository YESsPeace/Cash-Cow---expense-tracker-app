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
from database import get_categories_month_data, budget_data_read, \
    transaction_db_read, get_transaction_for_the_period, get_incomes_month_data, \
    incomes_db_read, categories_db_read, savings_db_read, get_savings_month_data


class BudgetMenu_in(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # date
        self.budget_data_date = str(config.current_menu_date)[:-3].replace('-', '')
        self.current_menu_date = config.current_menu_date
        self.days_in_current_menu_month = config.days_in_current_menu_month

        Clock.schedule_once(self.set_budgeted)

    def set_budgeted(self, *args):

        # Categories
        self.set_categories(self.budget_data_date)

        # Incomes
        self.set_incomes(self.budget_data_date)

        # Savings
        self.set_savings(self.budget_data_date)

    def set_savings(self, budget_data_date):
        savings_budget_data_dict = budget_data_read(id='savings_', db_name='budget_data_savings')
        type_dict = savings_db_read()

        print(f'savings_budget_data', *savings_budget_data_dict.items(), sep='\n')

        if budget_data_date in savings_budget_data_dict:
            budget_data_dict = savings_budget_data_dict[budget_data_date]

            savings_month_data_dict = \
                get_savings_month_data(
                    get_transaction_for_the_period(
                        from_date=str(self.current_menu_date.replace(day=1)),
                        to_date=str(self.current_menu_date.replace(day=self.days_in_current_menu_month)),
                        history_dict=transaction_db_read()
                    )
                )

            print(f'savings_month_data for {budget_data_date}', *savings_month_data_dict.items(), sep='\n')

            self.set_budget_menu(budget_data_dict, savings_month_data_dict,
                                 budget_menu_name='savings_budget',
                                 global_type_data_dict=type_dict)

            self.calculate_n_set_spent(budget_data_dict, savings_month_data_dict,
                                       progress_bar_name='all_savings_ProgressBar',
                                       spent_label_id='savings_label',
                                       budgeted_label_id='budgeted_savings_label')

            self.set_budget_list(budget_data_dict=budget_data_dict,
                                 budget_menu_name='savings_budget',
                                 global_type_data_dict=type_dict)

    def set_incomes(self, budget_data_date) -> None:
        incomes_budget_data_dict = budget_data_read(id='Income_', db_name='budget_data_incomes')
        type_dict = incomes_db_read()

        if budget_data_date in incomes_budget_data_dict:
            budget_data_dict = incomes_budget_data_dict[budget_data_date]

            incomes_month_data_dict = \
                get_incomes_month_data(
                    get_transaction_for_the_period(
                        from_date=str(self.current_menu_date.replace(day=1)),
                        to_date=str(self.current_menu_date.replace(day=self.days_in_current_menu_month)),
                        history_dict=transaction_db_read()
                    )
                )

            self.set_budget_menu(budget_data_dict, incomes_month_data_dict,
                                 budget_menu_name='incomes_budget',
                                 global_type_data_dict=type_dict)

            self.calculate_n_set_spent(budget_data_dict, incomes_month_data_dict,
                                       progress_bar_name='all_incomes_ProgressBar',
                                       spent_label_id='incomes_label',
                                       budgeted_label_id='budgeted_incomes_label')

            self.set_budget_list(budget_data_dict=budget_data_dict,
                                 budget_menu_name='incomes_budget',
                                 global_type_data_dict=type_dict)

    def set_categories(self, budget_data_date) -> None:
        categories_budget_data_dict = budget_data_read(id='Categories_', db_name='budget_data_categories')
        type_dict = categories_db_read()

        if budget_data_date in categories_budget_data_dict:
            budget_data_dict = categories_budget_data_dict[budget_data_date]

            categories_month_data_dict = \
                get_categories_month_data(
                    get_transaction_for_the_period(
                        from_date=str(self.current_menu_date.replace(day=1)),
                        to_date=str(self.current_menu_date.replace(day=self.days_in_current_menu_month)),
                        history_dict=transaction_db_read()
                    )
                )

            self.set_budget_menu(budget_data_dict, categories_month_data_dict,
                                 budget_menu_name='categories_budget',
                                 global_type_data_dict=type_dict)

            self.calculate_n_set_spent(budget_data_dict, categories_month_data_dict,
                                       progress_bar_name='all_categories_ProgressBar',
                                       spent_label_id='spent_label',
                                       budgeted_label_id='budgeted_label')

            self.set_budget_list(budget_data_dict=budget_data_dict,
                                 budget_menu_name='categories_budget',
                                 global_type_data_dict=type_dict)

    def set_budget_menu(self, budget_data_dict, month_data_dict, budget_menu_name,
                        global_type_data_dict, *args) -> None:
        for item_id in budget_data_dict:
            if item_id in month_data_dict:
                spent = int(month_data_dict[item_id]['SUM'])

            else:
                spent = 0

            progress = MDBoxLayout(
                MDBoxLayout(
                    MDLabel(
                        text=str(item_id) + ' ' +
                             str(global_type_data_dict[item_id]['Name']),
                        halign='left'
                    ),
                    MDLabel(
                        text=str(budget_data_dict[item_id]['Currency']) +
                             ' ' + str(
                            budget_data_dict[item_id]['Budgeted']),
                        halign='right'
                    ),
                ),
                MDScreen(
                    ProgressBar(
                        max=int(budget_data_dict[item_id]['Budgeted']),
                        value=spent,
                    ),
                    size_hint_y=1.25
                ),
                MDBoxLayout(
                    MDLabel(
                        text=str(spent),
                        font_style='Caption',
                        halign='left',
                    ),
                    MDLabel(
                        text='budgeted: ' +
                             str(budget_data_dict[item_id]['Currency']) +
                             ' ' + str(
                            budget_data_dict[item_id]['Budgeted']),
                        font_style='Caption',
                        halign='right',
                    ),
                ),
                id=str(item_id) + '_budget',
                md_bg_color=(.45, .3, .1, 1),
                orientation='vertical',
                size_hint_y=None,
                height=dp(60),
                padding=dp(3)
            )

            getattr(self.ids, budget_menu_name).add_widget(progress)

    def calculate_n_set_spent(self, budget_data_dict, month_data_dict, progress_bar_name,
                              spent_label_id, budgeted_label_id, *args) -> None:

        budgeted = sum([
            budget_data_dict[item_id]['Budgeted']
            for item_id in budget_data_dict
        ])

        spent = sum([
            month_data_dict[item_id]['SUM']
            for item_id in month_data_dict
            if item_id in budget_data_dict
        ])

        getattr(self.ids, progress_bar_name).value = \
            (spent / budgeted) * 100

        getattr(self.ids, spent_label_id).text = str(spent)

        getattr(self.ids, budgeted_label_id).text = str(budgeted)

    def set_budget_list(self, budget_data_dict, budget_menu_name,
                        global_type_data_dict, *args) -> None:
        if not (len(budget_data_dict) == len(global_type_data_dict)):
            self.Budget_grid = MDGridLayout(
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

            for item_id in global_type_data_dict:
                if item_id in budget_data_dict:
                    continue

                category = global_type_data_dict[item_id]

                self.Budget_grid.add_widget(
                    MDBoxLayout(
                        MDIconButton(
                            pos_hint={'center_x': 0.5, 'top': 0.5},
                            id=str(item_id),
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

            self.Budget_ScrollView = MDScrollView(
                self.Budget_grid,
                adaptive_height=True,
                size_hint=(1, None),
                height=dp(60),
            )

            getattr(self.ids, budget_menu_name).add_widget(self.Budget_ScrollView)

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
