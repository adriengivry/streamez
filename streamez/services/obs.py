import os
import subprocess

import psutil
from streamez.logging import Log
from streamez.settings import AppSettings

class OBSService:
    def __init__(self):
        self.process = None

    def initialize(self) -> bool:
        Log.info(">>> Initializing OBS Studio Service...")
        return True

    def start(self) -> bool:
        Log.info(">>> Running OBS Studio...")

        obs_executable = os.path.join(AppSettings.obs_folder, AppSettings.obs_executable_name)

        if not os.path.isfile(obs_executable):
            Log.error("OBS Studio executable not found. Please check the path.")
            return False
        
        try:
            if not AppSettings.obs_executable_name in (p.name() for p in psutil.process_iter()):
                # Run the executable
                self.process = subprocess.Popen([obs_executable] + AppSettings.obs_args, cwd=AppSettings.obs_folder)
                Log.info("OBS Studio launched successfully.")
            else:
                Log.warning("OBS Studio is already running.")

            return True
            
        except subprocess.CalledProcessError as e:
            Log.error(f"Failed to launch OBS Studio: {e}")
            return False
        except Exception as e:
            Log.error(f"An error occurred: {e}")
            return False

    def reload(self) -> bool:
        Log.info(">>> Reloading OBS Studio...")
        Log.info("Nothing to perform, all clear!")
        return True

    def stop(self) -> bool:
        Log.info(">>> Terminating OBS Studio...")

        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
            Log.info("OBS Studio terminated.")
        
        return True
    