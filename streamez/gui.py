import asyncio
import sys

from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QTimer

from streamez.application import Application
from streamez.utils import Utils, ServiceManagerState

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
        self.start_action = self.add_action("Start", self.on_start_button_clicked)
        self.stop_action = self.add_action("Stop", self.on_stop_button_clicked)
        self.reload_action = self.add_action("Reload", self.on_reload_button_clicked)
        self.menu.addSeparator()
        self.exit_action = self.add_action("Exit", self.on_exit_button_clicked)

        # Set the menu to the tray icon
        self.tray_icon.setContextMenu(self.menu)

        # Show the tray icon
        self.tray_icon.show()

        # Create and start the asyncio event loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.timer = QTimer()
        self.timer.timeout.connect(self.loop_iteration)
        self.timer.start(10)

    def add_action(self, label: str, on_clicked: object) -> QAction:
        action = QAction(label)
        action.setCheckable(False)
        action.triggered.connect(on_clicked)
        self.menu.addAction(action)
        return action

    def loop_iteration(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()

    def exec(self):
        async def run_sequence():
            self.update_actions(True)
            await self.run()
            self.update_actions()

        self.loop.create_task(run_sequence())
        sys.exit(self.app.exec())

    def update_actions(self, force_disable=False):
        self.initialize_action.setEnabled(not force_disable and self.state != ServiceManagerState.RUNNING)
        self.start_action.setEnabled(not force_disable and self.state != ServiceManagerState.RUNNING)
        self.stop_action.setEnabled(not force_disable and self.state == ServiceManagerState.RUNNING)
        self.reload_action.setEnabled(not force_disable and self.state == ServiceManagerState.RUNNING)
        self.exit_action.setEnabled(not force_disable)

    def on_initialize_button_clicked(self):
        async def initialize_sequence():
            self.update_actions(True)
            await self.initialize()
            self.update_actions()

        self.loop.create_task(initialize_sequence())

    def on_start_button_clicked(self):
        async def start_sequence():
            self.update_actions(True)
            await self.start()
            self.update_actions()

        self.loop.create_task(start_sequence())

    def on_stop_button_clicked(self):
        async def stop_sequence():
            self.update_actions(True)
            await self.stop()
            self.update_actions()

        self.loop.create_task(stop_sequence())

    def on_reload_button_clicked(self):
        async def reload_sequence():
            self.update_actions(True)
            await self.reload()
            self.update_actions()

        self.loop.create_task(reload_sequence())

    def on_exit_button_clicked(self):
        async def exit_sequence():
            self.update_actions(True)
            if self.state == ServiceManagerState.RUNNING:
                await self.stop()
            self.app.quit()

        self.loop.create_task(exit_sequence())
