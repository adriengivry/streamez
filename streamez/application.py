from enum import Enum

from streamez.services.elgato import ElgatoService
from streamez.services.hue import HueService
from streamez.services.obs import OBSService
from streamez.settings import AppSettings
from streamez.utils import ServiceManagerState

class Application:
    def __init__(self):
        self.state = ServiceManagerState.NONE

        self.obs_service = OBSService()
        self.hue_service = HueService()
        self.elgato_service = ElgatoService()

    async def run(self) -> bool:
        if AppSettings.target_initial_state == ServiceManagerState.READY or AppSettings.target_initial_state == ServiceManagerState.RUNNING:
            if await self.initialize():
                if AppSettings.target_initial_state == ServiceManagerState.RUNNING:
                    return await self.start()
            return False

    async def initialize(self) -> bool:
        assert self.state != ServiceManagerState.RUNNING, "Cannot initialize services while they are currently running!"

        if self.obs_service.initialize() and self.hue_service.initialize() and await self.elgato_service.initialize():
            self.state = ServiceManagerState.READY
            return True
        
        return False

    async def start(self) -> bool:
        assert self.state != ServiceManagerState.RUNNING, "Cannot start services while they are already running!"

        if not self.state == ServiceManagerState.READY:
            if not await self.initialize():
                return False

        if self.obs_service.start() and self.hue_service.start() and await self.elgato_service.start():
            self.state = ServiceManagerState.RUNNING
            return True
        
        return False

    async def stop(self) -> bool:
        assert self.state == ServiceManagerState.RUNNING, "Cannot stop services if they are not currently running!"

        if self.obs_service.stop() and self.hue_service.stop() and await self.elgato_service.stop():
            self.state = ServiceManagerState.READY
            return True
        
        return False

    async def reload(self) -> bool:
        assert self.state == ServiceManagerState.RUNNING, "Cannot reload services if they are not currently running!"

        if self.obs_service.reload() and self.hue_service.reload() and await self.elgato_service.reload():
            return True
        
        return False
