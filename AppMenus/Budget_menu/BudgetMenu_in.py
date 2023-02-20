from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.uix.progressbar import ProgressBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

import config
from AppData.data_scripts.GetData.Budget_data_scripts.GetCategoriesData import get_categories_budget_data


class BudgetMenu_in(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.categories_budget_data_dict = get_categories_budget_data(
            'AppData/data_files/Budget_files/' + str(config.current_menu_date)[:-3] + '/caregories-data.csv'
        )
        if not self.categories_budget_data_dict is None:
            print('Categories_Budget_data_dict in BudgetMenu', *self.categories_budget_data_dict.items(), sep='\n')
            Clock.schedule_once(self.set_categories_budget)

    def set_categories_budget(self, *args):
        for category_id in self.categories_budget_data_dict:
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
                      value=0
                  )
                ),
                MDBoxLayout(
                    MDLabel(
                        text='spent: None',
                        font_style='Caption',
                        halign='left',
                        valign='top'
                    ),
                    MDLabel(
                        text='budgeted: ' +
                             str(self.categories_budget_data_dict[category_id]['Currency']) +
                             ' ' + str(self.categories_budget_data_dict[category_id]['SUM']),
                        font_style='Caption',
                        halign='right',
                        valign='top'
                    ),
                ),
                id=str(category_id) + '_budget',
                md_bg_color=(.45, .3, .1, 1),
                orientation='vertical',
                size_hint_y=None,
                height=dp(60),
            )

            self.ids.categories_budget.add_widget(progress)
