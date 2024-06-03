from enum import Enum

from streamez.settings import AppSettings
from PySide6.QtWidgets import QMessageBox

class Log:
    @staticmethod
    def info(message: str):
        print(message)

    @staticmethod
    def warning(message: str):
        print(f"Warning: {message}")

    @staticmethod
    def error(message: str):
        print(f"Error: {message}")
        if AppSettings.show_message_box_on_error:
            QMessageBox.information(None, "Error", message)
        