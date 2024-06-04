from streamez.settings import Settings
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
        if Settings.get("show_message_box_on_error"):
            QMessageBox.critical(None, "Error", message)
        