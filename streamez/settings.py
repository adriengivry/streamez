import os
import json

from streamez.utils import Utils

class Settings:
    user_settings = dict()

    default_settings = {
        "auto_initialize_on_service_start" : True,
        "show_message_box_on_error": True,
        "obs_folder": os.path.join("C:", os.sep, "Program Files", "obs-studio", "bin", "64bit"),
        "obs_executable_name": "obs64.exe",
        "obs_args": [],
        "elgato_lights": [],
        "hue_bridge_address": None,
        "hue_lights": []
    }

    @staticmethod
    def get(setting_name: str):
        return Settings.user_settings.get(setting_name, Settings.default_settings.get(setting_name))

    @staticmethod
    def get_user_settings_file_path(create_if_not_exist: bool = False):
        settings_file = os.path.join(Utils.get_appdata_path(), 'settings.json')
        if create_if_not_exist and not os.path.exists(settings_file):
            os.makedirs(os.path.dirname(settings_file), exist_ok=True)
            with open(settings_file, 'w') as f:
                json.dump({}, f, indent=4)
        return settings_file

    @staticmethod
    def load_user_settings():
        settings_file = Settings.get_user_settings_file_path(True)

        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                Settings.user_settings = json.load(f)
