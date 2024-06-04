import asyncio

from elgato import Elgato, State

from streamez.logging import Log
from streamez.services.service import IService
from streamez.settings import Settings

class ElgatoService(IService):
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
        
    def should_skip(self) -> bool:
        return len(Settings.get("elgato_lights")) == 0
        
    def initialize(self) -> bool:
        Log.info(">>> Initializing Elgato service...")

        async def initialize_sequence() -> bool:
            try:
                self.elgato_lights_backup_settings.clear()
                for light in Settings.get("elgato_lights"):
                    state = await self.get_elgato_light_state(light['address'])
                    self.elgato_lights_backup_settings.append({
                        "address": light['address'],
                        "state": state
                    })
                return True
            except Exception as e:
                Log.error(f"An error occurred: {e}")
                return False
            
        return asyncio.run(initialize_sequence())
        
    def start(self) -> bool:
        Log.info(">>> Setting up Elgato lights...")

        async def start_sequence() -> bool:
            try:
                for light in Settings.get("elgato_lights"):
                    await self.set_elgato_light_state(light['address'], light['state'])
                return True
            except Exception as e:
                Log.error(f"An error occurred: {e}")
                return False
            
        return asyncio.run(start_sequence())

    def reload(self) -> bool:
        Log.info(">>> Reloading Elgato lights...")

        async def reload_sequence() -> bool:
            try:
                for light in Settings.get("elgato_lights"):
                    await self.set_elgato_light_state(light['address'], light['state'])
                return True
            except Exception as e:
                Log.error(f"An error occurred: {e}")
                return False
            
        return asyncio.run(reload_sequence())

    def stop(self) -> bool:
        Log.info(">>> Resetting Elgato lights...")

        async def stop_sequence() -> bool:
            try:
                for light in self.elgato_lights_backup_settings:
                    await self.set_elgato_light_state(light['address'], light['state'])
                return True
            except Exception as e:
                Log.error(f"An error occurred: {e}")
                return False
            
        return asyncio.run(stop_sequence())

        