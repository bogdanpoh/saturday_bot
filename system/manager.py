import os
import platform
import config
from helpers import constants
from helpers.switch import Switch


class SystemManager:

    @staticmethod
    def is_mac_os():
        return platform.system() == constants.mac_os_identifier

    @staticmethod
    def device_name() -> str:
        name = platform.node().split(".")[0]
        return name

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
    def sound_level() -> int:
        if SystemManager.is_mac_os():
            outpus = os.popen("osascript -e 'get volume settings'").readlines()[-1]
            sound_level = outpus.split(",")[0].split(":")[-1]
            return int(sound_level)

    @staticmethod
    def set_volume(value):
        if SystemManager.is_mac_os():
            command = f"sudo osascript -e 'set volume {value}'"
            os.system(f"echo {config.computer_password} | sudo -S {command}")

    @staticmethod
    def battery_charg():
        if SystemManager.is_mac_os():
            outputs = os.popen("pmset -g batt").readlines()[-1]
            battery_charg = outputs.split("\t")[-1].split(";")[0]
            return battery_charg

    # for use this command, need install https://github.com/nriley/brightness
    @staticmethod
    def brightness_level() -> int:
        if SystemManager.is_mac_os():
            outputs = os.popen("brightness -l").readlines()[1]
            brightness_level = int(float(outputs.split(" ")[-1]) * 100)
            return brightness_level

    # for use this command, need install https://github.com/nriley/brightness
    @staticmethod
    def set_brightness(value):
        if SystemManager.is_mac_os():
            command = f"brightness {value}"
            os.system(command)