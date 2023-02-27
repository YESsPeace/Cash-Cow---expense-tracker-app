from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.progressbar import ProgressBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

import config
from AppData.data_scripts.GetData.Budget_data_scripts.GetCategoriesData import get_categories_budget_data
from AppData.data_scripts.GetData.GetCategoriesMonthData import get_categories_month_data
from AppData.data_scripts.GetData.GetHistoryDataForThePeriod import get_transaction_for_the_period, \
    get_transaction_history


class BudgetMenu_in(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.all_categories_spent = 0

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

    def set_categories_budget(self, *args) -> None:
        for category_id in self.categories_budget_data_dict:
            if category_id in self.categories_month_data_dict:
                spent = int(self.categories_month_data_dict[category_id]['SUM'])

                self.all_categories_spent += \
                    (spent / int(self.categories_budget_data_dict[category_id]['SUM']))

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
        Clock.schedule_once(self.calculate_n_set_categories_spent)

    def calculate_n_set_categories_spent(self, *args) -> None:
        print('All categories spent:',
              self.all_categories_spent / len(self.categories_budget_data_dict))
        self.ids.all_categories_ProgressBar.value = \
            (self.all_categories_spent / len(self.categories_budget_data_dict)) * 100

    def set_categories_list(self, *args) -> None:
        self.category_grid = MDGridLayout(
            MDBoxLayout(
                MDIconButton(
                    pos_hint={'center_x': 0.5, 'top': 0.5},
                    md_bg_color=(.66, .66, .66, 1),
                    icon_size=dp(15),
                    on_release=self.open_categories_grid,
                ),
                MDLabel(
                    text='More',
                    size_hint=(1, .25),
                    halign='center',
                ),
                orientation='vertical',
                size_hint_y=None,
                height=dp(60)
            ),
            md_bg_color=(.3, .5, .4, 1),
            size_hint_y=None,
            adaptive_height=True,
            cols=4,
        )

        for category_id in config.global_categories_data_dict:
            if category_id in self.categories_budget_data_dict:
                continue

            category = config.global_categories_data_dict[category_id]

            self.category_grid.add_widget(
                MDBoxLayout(
                    MDIconButton(
                        pos_hint={'center_x': 0.5, 'top': 0.5},
                        id=str(category_id),
                        md_bg_color=category['Color'][:-1] + (1,),
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

    def open_categories_grid(self, *args) -> None:
        print('Open pressed')

        self.category_ScrollView.size = self.category_grid.size

        self.category_grid.children[-1].clear_widgets()

        self.category_grid.children[-1].add_widget(
            MDIconButton(
                pos_hint={'center_x': 0.5, 'top': 0.5},
                md_bg_color=(.66, .66, .66, 1),
                icon_size=dp(15),
                on_release=self.close_categories_grid,
            ),
        )

        self.category_grid.children[-1].add_widget(
            MDLabel(
                text='Less',
                size_hint=(1, .25),
                halign='center',
            ),
        )

    def close_categories_grid(self, *args) -> None:
        print('Close pressed')

        self.category_ScrollView.height = dp(60)

        self.category_grid.children[-1].clear_widgets()

        self.category_grid.children[-1].add_widget(
            MDIconButton(
                pos_hint={'center_x': 0.5, 'top': 0.5},
                md_bg_color=(.66, .66, .66, 1),
                icon_size=dp(15),
                on_release=self.open_categories_grid,
            ),
        )

        self.category_grid.children[-1].add_widget(
            MDLabel(
                text='More',
                size_hint=(1, .25),
                halign='center',
            ),
        )
