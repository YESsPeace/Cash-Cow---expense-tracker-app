import os
import pathlib
import shutil
import sys
from plyer import storagepath

from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.screen import MDScreen

from BasicMenus.CustomWidgets import TopNotification, ErrorNotification


def get_download_path():
    try:
        return str(storagepath.get_downloads_dir())

    except Exception as error:
        ErrorNotification(text=f"Error: {error}").open()

        return str(os.path.dirname(os.path.abspath(sys.argv[0]).replace('\\', '/')))


class ExportMenu(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = get_download_path()
        print(self.path)

    def import_button_clicked(self):
        self.open_file_manager()

    def export_button_clicked(self):
        self.export_app_data()

    def open_file_manager(self):
        def exit_manager(*args):
            self.file_manager.close()

        def select_path(path):
            self.file_manager.close()

            if path[-3:] == '.db':
                self.import_app_data(path)

        try:
            self.file_manager = MDFileManager(
                exit_manager=exit_manager,
                select_path=select_path,
                preview=False
            )

            self.file_manager.show(self.path)

        except Exception as error:
            ErrorNotification(text=f"Error: {error}").open()

    def import_app_data(self, path_to_file, *args):
        try:
            shutil.copy(path_to_file, 'AppDataBase.db')
            TopNotification(text=f'Everything went well, please restart the app').open()

        except Exception as error:
            ErrorNotification(text=f"Error: {error}").open()

    def export_app_data(self, path_to_file=None):
        if path_to_file is None:
            path_to_file = self.path

        filename = 'AppDataBase.db'

        try:
            shutil.copy(filename, path_to_file + '/Cash-Cow.db')

            TopNotification(text=f'File Cash-Cow.db exported to {path_to_file}').open()

        except Exception as error:
            ErrorNotification(text=f"Error: {error}").open()
