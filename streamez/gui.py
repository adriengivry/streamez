import asyncio
import sys

from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QTimer

from streamez.application import Application
from streamez.logging import Log
from streamez.settings import Settings
from streamez.utils import Utils, ServiceManagerState
import os
import subprocess

class SystemTrayApp(Application):
    def __init__(self):
        super().__init__()

        self.app = QApplication(sys.argv)
        self.tray_icon = QSystemTrayIcon()

        # Set the icon for the system tray
        self.tray_icon.setIcon(QIcon(Utils.get_bundled_asset("icon.ico")))  # Replace with your icon path

        # Create the menu
        self.menu = QMenu()

        self.initialize_action = self.add_action("Initialize", self.on_initialize_button_clicked)
        self.intiailize_separator = self.menu.addSeparator()
        self.start_action = self.add_action("Start", self.on_start_button_clicked)
        self.stop_action = self.add_action("Stop", self.on_stop_button_clicked)
        self.reload_action = self.add_action("Reload", self.on_reload_button_clicked)
        self.menu.addSeparator()
        self.open_settings_action = self.add_action("Open Settings", self.on_open_settings_clicked)
        self.reload_settings_action = self.add_action("Reload Settings", self.on_reload_settings_clicked)
        self.menu.addSeparator()
        self.exit_action = self.add_action("Exit", self.on_exit_button_clicked)

        self.app.setQuitOnLastWindowClosed(False)

        # Set the menu to the tray icon
        self.tray_icon.setContextMenu(self.menu)

        # Show the tray icon
        self.tray_icon.show()

    def add_action(self, label: str, on_clicked: object) -> QAction:
        action = QAction(label)
        action.setCheckable(False)
        action.triggered.connect(on_clicked)
        self.menu.addAction(action)
        return action

    def run(self):
        self.update_actions()
        sys.exit(self.app.exec())

    def update_actions(self, force_disable=False):
        auto_init_on_start = Settings.get("auto_initialize_on_service_start")

        self.initialize_action.setVisible(not auto_init_on_start)
        self.intiailize_separator.setVisible(not auto_init_on_start)
        self.initialize_action.setEnabled(not force_disable and self.state != ServiceManagerState.RUNNING)
        self.start_action.setEnabled(not force_disable and (self.state == ServiceManagerState.READY or (auto_init_on_start and self.state == ServiceManagerState.NONE)))
        self.stop_action.setEnabled(not force_disable and self.state == ServiceManagerState.RUNNING)
        self.reload_action.setEnabled(not force_disable and self.state == ServiceManagerState.RUNNING)
        self.reload_settings_action.setEnabled(not force_disable and self.state != ServiceManagerState.RUNNING)
        self.exit_action.setEnabled(not force_disable)

    def on_initialize_button_clicked(self):
        self.update_actions(True)
        self.initialize()
        self.update_actions()

    def on_start_button_clicked(self):
        self.update_actions(True)
        self.start()
        self.update_actions()

    def on_stop_button_clicked(self):
        self.update_actions(True)
        self.stop()
        self.update_actions()

    def on_reload_button_clicked(self):
        self.update_actions(True)
        self.reload()
        self.update_actions()

    def on_open_settings_clicked(self):
        settings_file = Settings.get_user_settings_file_path(True)

        if os.path.exists(settings_file):
            subprocess.Popen(["start", settings_file], shell=True)
        else:
            Log.error("The settings file does not exist!")

    def on_reload_settings_clicked(self):
        self.load_settings()
        self.update_actions()

    def on_exit_button_clicked(self):
        self.update_actions(True)
        if self.state == ServiceManagerState.RUNNING:
            self.stop()
        self.app.quit()
