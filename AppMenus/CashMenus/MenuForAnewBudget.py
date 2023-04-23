from kivy.graphics import Color, Rectangle
from kivy.properties import BooleanProperty, OptionProperty
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivy.clock import Clock

import config
from AppMenus.Budget_menu.BudgetMenu_in import BudgetMenu_in
from AppMenus.other_func import calculate, update_menus
from database import budget_data_write, budget_data_cut, budget_data_edit


class menu_for_a_new_budget(MDNavigationDrawer):
    state = OptionProperty("open", options=("close", "open"))
    status = OptionProperty(
        "opened",
        options=(
            "closed",
            "opening_with_swipe",
            "opening_with_animation",
            "opened",
            "closing_with_swipe",
            "closing_with_animation",
        ),
    )
    enable_swiping = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        self.currency = '₽'

        self.default_sum_label_text = f'{self.currency} 0'

        self.current_menu_date = config.current_menu_date

        self.item = config.item

        print(*self.item.items(), sep='\n')

        super().__init__(*args, **kwargs)

        with self.canvas.before:
            Color(0, 0, 0, .5)
            Rectangle(size=config.main_screen_size, pos=config.main_screen_pos)

        Clock.schedule_once(self.set_widgets_prop)

    def set_widgets_prop(self, *args):
        self.set_progressbar_value(self, *args)
        self.set_button_color(self, *args)
        self.set_current_budgeted(self, *args)

    def update_status(self, *_) -> None:
        status = self.status
        if status == "closed":
            self.state = "close"
        elif status == "opened":
            self.state = "open"
        elif self.open_progress == 1 and status == "opening_with_animation":
            self.status = "opened"
            self.state = "open"
        elif self.open_progress == 0 and status == "closing_with_animation":
            self.status = "closed"
            self.state = "close"

            self.del_myself()

        elif status in (
                "opening_with_swipe",
                "opening_with_animation",
                "closing_with_swipe",
                "closing_with_animation",
        ):
            pass
        if self.status == "closed":
            self.opacity = 0
        else:
            self.opacity = 1

    def del_myself(self):
        self.parent.remove_widget(self)

    def sign_btn_pressed(self, btn):
        if len(set(self.ids.sum_label.text).intersection({'+', '-', '÷', 'x'})):
            self.calculate_btn_pressed()
            self.ids.sum_label.text = self.ids.sum_label.text + btn.text

        elif self.ids.sum_label.text[-1] in ['+', '-', '÷', 'x']:
            self.ids.sum_label.text = self.ids.sum_label.text[:-1] + btn.text

        else:
            self.ids.sum_label.text = self.ids.sum_label.text + btn.text

        self.ids.done_btn.text = '='

    def calculate_btn_pressed(self):
        self.ids.sum_label.text = f'{self.currency} {calculate(self.ids.sum_label.text)}'

    def write_budget_into_db(self, budgeted_sum, *args):
        # menu
        self.status = 'closed'

        # getting sum for budget
        budgeted_sum = budgeted_sum[2:]  # del currency

        item_type = str(self.item['id']).split('_')[0].lower()

        if budgeted_sum[-1] == '.':
            budgeted_sum = budgeted_sum[:-1]

        try:
            budgeted_sum = int(budgeted_sum)

        except ValueError:
            budgeted_sum = float(budgeted_sum)

        # the values were got in the __init__
        budget_data = {
            'id': int(str(self.item['id']).split('_')[-1]),
            'date': str(self.current_menu_date).replace('-', '')[:-2],
            'Budgeted': budgeted_sum,
            'currency': 'RUB',
        }
        if budgeted_sum > 0:
            if self.item['Budgeted'] == 0:
                # writing into the database
                budget_data_write(
                    db_name=f'budget_data_{item_type}',
                    data_dict=budget_data
                )

            else:
                budget_data_edit(
                    db_name=f'budget_data_{item_type}',
                    data_dict=budget_data
                )

        else:
            budget_data_cut(
                db_name=f'budget_data_{item_type}',
                data_dict=budget_data
            )

        update_menus(str(self.current_menu_date))

    def set_progressbar_value(self, *args):

        sum, budgeted = self.item['SUM'], self.item['Budgeted']

        if budgeted != 0:
            value_ = (sum / budgeted) * 100

        else:
            value_ = 0

        self.ids.progress_bar.value = value_

    def set_button_color(self, *args):

        color = self.item['Color'][:-1] + [1]

        self.ids.budget_item_icon_button.md_bg_color = color

    def set_current_budgeted(self, *args):
        current_budgeted = self.item['Budgeted']
        self.ids.sum_label.text = f'{self.currency} {current_budgeted}'
