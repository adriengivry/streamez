from elgato import Elgato, State

from streamez.logging import Log
from streamez.settings import AppSettings, ElgatoLightDesc

class ElgatoService:
    def __init__(self):
        self.elgato_lights_backup_settings = list()
        
    async def set_elgato_light_state(self, address, state):
        async with Elgato(address) as elgato:
            await elgato.light(on=state)
            Log.info("Elgato light (" + address + ") state set to: " + ("ON" if state else "OFF"))
            
    async def get_elgato_light_state(self, address) -> bool:
        async with Elgato(address) as elgato:
            state: State = await elgato.state()
            return state.on
    
    async def initialize(self) -> bool:
        Log.info(">>> Initializing Elgato service...")

        try:
            self.elgato_lights_backup_settings.clear()
            for light in AppSettings.elgato_lights:
                self.elgato_lights_backup_settings.append(ElgatoLightDesc(light.address, await self.get_elgato_light_state(light.address)))
            return True
        except Exception as e:
            Log.error(f"An error occurred: {e}")
            return False
        
    async def start(self) -> bool:
        Log.info(">>> Setting up Elgato lights...")
        try:
            for light in AppSettings.elgato_lights:
                await self.set_elgato_light_state(light.address, light.state)
            return True
        except Exception as e:
            Log.error(f"An error occurred: {e}")
            return False

    async def reload(self) -> bool:
        Log.info(">>> Reloading Elgato lights...")
        try:
            for light in AppSettings.elgato_lights:
                await self.set_elgato_light_state(light.address, light.state)
            return True
        except Exception as e:
            Log.error(f"An error occurred: {e}")
            return False

    async def stop(self) -> bool:
        Log.info(">>> Resetting Elgato lights...")
        try:
            for light in self.elgato_lights_backup_settings:
                await self.set_elgato_light_state(light.address, light.state)
            return True
        except Exception as e:
            Log.error(f"An error occurred: {e}")
            return False
        