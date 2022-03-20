import os
from platform import system
from helpers import constants
import config


class SystemManager:

    @staticmethod
    def is_mac_os():
        return system() == constants.mac_os_identifier

    @staticmethod
    def list_shortcuts():
        if SystemManager.is_mac_os():
            outputs = os.popen("Shortcuts list").readlines()
            shortcuts = map(lambda shortcut: str(shortcut).replace("\n", ""), outputs)
            return shortcuts
        else:
            return None

    @staticmethod
    def run_shortcut(shortcut):
        if SystemManager.is_mac_os():
            command = f"Shortcuts run '{shortcut}'"
            os.system(f"echo {config.computer_password} | sudo -S {command}")

    @staticmethod
    def set_volume(value):
        if SystemManager.is_mac_os():
            command = f"sudo osascript -e 'set volume {value}'"
            os.system(f"echo {config.computer_password} | sudo -S {command}")
