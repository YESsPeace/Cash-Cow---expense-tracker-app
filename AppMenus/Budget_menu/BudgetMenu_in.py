from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.uix.progressbar import ProgressBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

import config
from AppData.data_scripts.GetData.Budget_data_scripts.GetCategoriesData import get_categories_budget_data
from AppData.data_scripts.GetData.GetCategoriesMonthData import get_categories_month_data
from AppData.data_scripts.GetData.GetHistoryDataForThePeriod import get_transaction_for_the_period, \
    get_transaction_history


class BudgetMenu_in(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.categories_month_data_dict = \
            get_categories_month_data(get_transaction_for_the_period(
                from_date=str(config.current_menu_date.replace(day=1)),
                to_date=str(config.current_menu_date.replace(day=config.days_in_current_menu_month)),
                history_dict=get_transaction_history(
                    history_file_path='AppData/data_files/transaction-history.csv',
                )
            )
            )

        print('Categories_month_Budget_data_dict in BudgetMenu', *self.categories_month_data_dict.items(), sep='\n')

        self.categories_budget_data_dict = get_categories_budget_data(
            'AppData/data_files/Budget_files/' + str(config.current_menu_date)[:-3] + '/caregories-data.csv'
        )
        if not self.categories_budget_data_dict is None:
            print('Categories_Budget_data_dict in BudgetMenu', *self.categories_budget_data_dict.items(), sep='\n')
            Clock.schedule_once(self.set_categories_budget)

    def set_categories_budget(self, *args):
        for category_id in self.categories_budget_data_dict:
            if category_id in self.categories_month_data_dict:
                spent = int(self.categories_month_data_dict[category_id]['SUM'])

            else:
                spent = 0


            progress = MDBoxLayout(
                MDBoxLayout(
                    MDLabel(
                        text=str(category_id),
                        halign='left'
                    ),
                    MDLabel(
                        text=str(self.categories_budget_data_dict[category_id]['Currency']) +
                             ' ' + str(self.categories_budget_data_dict[category_id]['SUM']),
                        halign='right'
                    ),
                ),
                MDScreen(
                    ProgressBar(
                        max=int(self.categories_budget_data_dict[category_id]['SUM']),
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
                             str(self.categories_budget_data_dict[category_id]['Currency']) +
                             ' ' + str(self.categories_budget_data_dict[category_id]['SUM']),
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

    def set_categories_list(self, *args):
        category_grid = MDGridLayout(
            md_bg_color=(.3, .5, .4, 1),
            size_hint_y=None,
            adaptive_height=True,
        )

        self.ids.categories_budget.add_widget(category_grid)
