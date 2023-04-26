import config
from AppMenus.Categories_menu.Menu_For_new_category.icon_choice_menu import icon_choice_menu
from AppMenus.other_func import update_menus
from BasicMenus import MenuForEditItemBase
from BasicMenus.CustomWidgets import TopNotification
from database import db_data_delete, db_data_edit, db_data_add


class menu_for_new_or_edit_category(MenuForEditItemBase):
    def __init__(self, *args, **kwargs):
        self.item = config.category_item

        print(*self.item.items(), sep='\n')

        super().__init__(*args, **kwargs)

    def complete_pressed(self, *args):
        self.item['Name'] = self.ids.category_name_text_field.text

        if self.item.get('new') is True:
            self.create_category()

        elif self.item.values() != config.item.values():
            self.edit_category()

        else:
            self.del_myself()
            TopNotification(text="There's nothing to do").open()

    def create_category(self, *args):
        print('# creating category started')
        self.item['Name'] = self.ids.category_name_text_field.text

        db_data_add(
            db_name=self.item['db_name'],
            params=self.item
        )

        update_menus(str(config.current_menu_date))
        self.del_myself()
        TopNotification(text="Category created").open()

    def edit_category(self, *args):
        print('# editing category started')
        db_data_edit(
            db_name=self.item['db_name'],
            item_id=self.item['ID'],
            name=self.ids.category_name_text_field.text,
            icon=self.item['Icon'],
            color=self.item['Color']
        )

        update_menus(str(config.current_menu_date))
        self.del_myself()
        TopNotification(text="Category edited").open()

    def delete_category(self, *args):
        if self.item['new'] is True:
            TopNotification(text="Category not yet created to be deleted").open()
            return

        print('# deleting category started')
        db_data_delete(
            db_name=self.item['db_name'],
            item_id=self.item['ID']
        )
        update_menus(str(config.current_menu_date))
        self.del_myself()
        TopNotification(text="Category deleted").open()

    def open_icon_choice_menu(self, *args):
        self.add_widget(icon_choice_menu())

