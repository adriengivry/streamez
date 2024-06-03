from enum import Enum
import os

class ServiceManagerState(Enum):
    NONE = 1
    READY = 2
    RUNNING = 3
    
class Utils:
    @staticmethod
    def get_bundle_dir():
        return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    @staticmethod
    def get_bundled_asset(asset_path):
        return os.path.join(Utils.get_bundle_dir(), asset_path)