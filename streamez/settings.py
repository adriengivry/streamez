import os
from dataclasses import dataclass

from streamez.utils import ServiceManagerState

@dataclass
class HueLightDesc:
    name: str
    on: bool
    brightness: int
    hue: int
    saturation: int

@dataclass
class ElgatoLightDesc:
    address: str
    state: bool

class AppSettings:
    # General
    target_initial_state = ServiceManagerState.NONE
    show_message_box_on_error = True
    
    # OBS Studio
    obs_folder = os.path.join("C:", os.sep, "Program Files", "obs-studio", "bin", "64bit")
    obs_executable_name = "obs64.exe"
    obs_args = ["--startvirtualcam", "--scene", "Default", "--minimize-to-tray", "--disable-shutdown-check", "--disable-updater"]

    # Elgato
    elgato_lights = [
        ElgatoLightDesc("192.168.2.38", True),
        ElgatoLightDesc("192.168.2.21", True)
    ]

    # Philips Hue
    hue_bridge_address = "192.168.2.14"
    hue_lights = [
        HueLightDesc("Office Floor", True, 254, 38146, 7),
        HueLightDesc("Hue go", True, 254, 38146, 7),
    ]
