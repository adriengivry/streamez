from phue import Bridge

from streamez.logging import Log
from streamez.services.service import IService
from streamez.settings import Settings

class HueService(IService):
    def __init__(self):
        self.hue_lights_backup_settings = list()

    def set_hue_light(self, light, config):
        light.on = config['on']
        light.brightness = config['brightness']
        light.hue = config['hue']
        light.saturation = config['saturation']
        Log.info("Hue light (" + light.name + ") set to: on=" + str(light.on) + ", brightness=" + str(light.brightness) + ", hue=" + str(light.hue) + ", saturation=" + str(light.saturation))

    def get_bridge(self):
        bridge = Bridge(Settings.get("hue_bridge_address"))
        bridge.connect()
        return bridge
    
    def get_lights(self):
        try:
            bridge = self.get_bridge()
            return bridge.get_light_objects('name')
        except Exception as e:
            bridge_address = Settings.get('hue_bridge_address')
            error_message = f"Failed to retrieve lights from the Philips Hue Bridge on IP: [{bridge_address}]. Please check the bridge's IP address, ensure that the bridge is accessible, and (if it's your first connection) that you pressed its button in the past 30 seconds.\n\nError details:\n{e}"
            Log.error(error_message)
            return None
        
    def should_skip(self) -> bool:
        return not Settings.get("hue_bridge_address") and len(Settings.get("hue_lights")) == 0
        
    def initialize(self) -> bool:
        Log.info(">>> Initializing Hue service...")
        try:
            self.hue_lights_backup_settings.clear()

            lights = self.get_lights()
            if lights == None:
                return False
            
            for light in Settings.get("hue_lights"):
                light_name = light['name']
                target_light = lights[light_name]
                self.hue_lights_backup_settings.append({
                    "name": light_name,
                    "on": target_light.on,
                    "brightness": target_light.brightness,
                    "hue": target_light.hue,
                    "saturation": target_light.saturation
                })
                
            return True
        except Exception as e:
            Log.error(f"An error occurred: {e}")
            return False

    def start(self) -> bool:
        Log.info(">>> Setting up Hue lights...")
        try:
            lights = self.get_lights()
            if lights == None:
                return False
            
            for light in Settings.get("hue_lights"):
                self.set_hue_light(lights[light['name']], light)

            return True
        except Exception as e:
            Log.error(f"An error occurred: {e}")
            return False

    def reload(self) -> bool:
        Log.info(">>> Reloading Hue lights...")
        try:
            lights = self.get_lights()
            if lights == None:
                return False
            
            for light in Settings.get("hue_lights"):
                self.set_hue_light(lights[light['name']], light)

            return True
        except Exception as e:
            Log.error(f"An error occurred: {e}")
            return False

    def stop(self) -> bool:
        Log.info(">>> Resetting Hue lights...")
        try:
            lights = self.get_lights()
            if lights == None:
                return False
            
            for light in self.hue_lights_backup_settings:
                self.set_hue_light(lights[light['name']], light)

            return True
        except Exception as e:
            Log.error(f"An error occurred: {e}")
            return False
