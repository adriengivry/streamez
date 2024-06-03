from phue import Bridge

from streamez.logging import Log
from streamez.settings import AppSettings, HueLightDesc

class HueService:
    def __init__(self):
         self.hue_lights_backup_settings = list()

    def set_hue_light(self, light, config):
            light.on = config.on
            light.brightness = config.brightness
            light.hue = config.hue
            light.saturation = config.saturation
            Log.info("Hue light (" + light.name + ") set to: on=" + str(config.on) + ", brightness=" + str(config.brightness) + ", hue=" + str(config.hue) + ", saturation=" + str(config.saturation))

    def get_bridge(self):
        bridge = Bridge(AppSettings.hue_bridge_address)
        bridge.connect()
        return bridge
    
    def get_lights(self):
        bridge = self.get_bridge()
        return bridge.get_light_objects('name')
    
    def initialize(self) -> bool:
        Log.info(">>> Initializing Hue service...")
        try:
            self.hue_lights_backup_settings.clear()
            lights = self.get_lights()
            for light in AppSettings.hue_lights:
                self.hue_lights_backup_settings.append(HueLightDesc(
                    light.name,
                    lights[light.name].on,
                    lights[light.name].brightness,
                    lights[light.name].hue,
                    lights[light.name].saturation
                ))
            return True
        except Exception as e:
            Log.error(f"An error occurred: {e}")
            return False

    def start(self) -> bool:
        Log.info(">>> Setting up Hue lights...")
        try:
            lights = self.get_lights()
            for light in AppSettings.hue_lights:
                self.set_hue_light(lights[light.name], light)
            return True
        except Exception as e:
            Log.error(f"An error occurred: {e}")
            return False

    def reload(self) -> bool:
        Log.info(">>> Reloading Hue lights...")
        try:
            lights = self.get_lights()
            for light in AppSettings.hue_lights:
                self.set_hue_light(lights[light.name], light)
            return True
        except Exception as e:
            Log.error(f"An error occurred: {e}")
            return False

    def stop(self) -> bool:
        Log.info(">>> Resetting Hue lights...")
        try:
            lights = self.get_lights()
            for light in self.hue_lights_backup_settings:
                self.set_hue_light(lights[light.name], light)
            return True
        except Exception as e:
            Log.error(f"An error occurred: {e}")
            return False
