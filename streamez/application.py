from enum import Enum

from streamez.services.elgato import ElgatoService
from streamez.services.hue import HueService
from streamez.services.obs import OBSService
from streamez.services.service import IService
from streamez.settings import Settings
from streamez.utils import ServiceManagerState

class Application:
    def __init__(self):
        self.state = ServiceManagerState.NONE
        self.load_settings()
        self.register_services()

    def register_services(self):
        self.services = list[IService]([
            OBSService(),
            HueService(),
            ElgatoService()
        ])
        
    def load_settings(self):
        Settings.load_user_settings()
        self.state = ServiceManagerState.NONE

    def initialize(self) -> bool:
        assert self.state != ServiceManagerState.RUNNING, "Cannot initialize services while they are currently running!"

        for service in self.services:
            if not service.should_skip() and not service.initialize():
                return False
            
        self.state = ServiceManagerState.READY
        return True

    def start(self) -> bool:
        if Settings.get("auto_initialize_on_service_start"):
            if not self.initialize():
                return False

        assert self.state != ServiceManagerState.RUNNING, "Cannot start services while they are already running!"
        assert self.state == ServiceManagerState.READY, "Cannot start services before initializing them!"

        for service in self.services:
            if not service.should_skip() and not service.start():
                return False
            
        self.state = ServiceManagerState.RUNNING
        return True

    def stop(self) -> bool:
        assert self.state == ServiceManagerState.RUNNING, "Cannot stop services if they are not currently running!"

        for service in self.services:
            if not service.should_skip() and not service.stop():
                return False
        
        self.state = ServiceManagerState.READY
        return True

    def reload(self) -> bool:
        assert self.state == ServiceManagerState.RUNNING, "Cannot reload services if they are not currently running!"

        for service in self.services:
            if not service.should_skip() and not service.reload():
                return False
        
        return True
