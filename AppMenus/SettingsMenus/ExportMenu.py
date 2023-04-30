import os.path
import shutil
import sys

from kivy.utils import platform
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.screen import MDScreen

from BasicMenus.CustomWidgets import TopNotification


class ExportMenu(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_manager = None
        self.path = os.path.dirname(os.path.abspath(sys.argv[0]).replace('\\', '/'))
        print(self.path)

    def open_file_manager(self):
        def exit_manager(*args):
            self.file_manager.close()

        def select_path(path):
            self.file_manager.close()

            if path[-3:] == '.db':
                self.import_app_data(path)

        self.file_manager = MDFileManager(
            exit_manager=exit_manager,
            select_path=select_path,
            preview=False
        )

        self.file_manager.show(self.path)

    def import_app_data(self, path_to_file, *args):
        filename = 'AppDataBase.db'
        try:
            shutil.copy(path_to_file, filename)
            TopNotification(text=f'Everything went well, please restart the app').open()

        except:
            TopNotification(text=f'Something went wrong').open()

    def export_app_data(self):
        filename = 'AppDataBase.db'
        path = 'Cash_cow.db'

        try:
            if platform == 'android':
                path = '/storage/emulated/0/Download/Cash_cow.db'

            shutil.copy(filename, path)

            TopNotification(text=f'File {filename} exported to Download').open()

        except:
            TopNotification(text='Something went wrong').open()
