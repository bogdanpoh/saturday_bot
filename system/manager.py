import os
import platform
import config
from pynput.keyboard import Key, Controller
from helpers import constants
from helpers.switch import Switch


class SystemManager:

    @staticmethod
    def is_mac_os():
        return platform.system() == constants.mac_os_identifier

    @staticmethod
    def device_name():
        name = platform.node().split(".")[0]
        if name:
            return name
        else:
            return None

    @staticmethod
    def list_shortcuts():
        if SystemManager.is_mac_os():
            outputs = os.popen("Shortcuts list").readlines()
            shortcuts = map(lambda shortcut: str(shortcut).replace("\n", ""), outputs)
            return list(shortcuts)
        else:
            return None

    @staticmethod
    def run_shortcut(shortcut):
        if SystemManager.is_mac_os():
            command = f"Shortcuts run '{shortcut}'"
            os.system(f"echo {config.computer_password} | sudo -S {command}")

    @staticmethod
    def sound_level():
        if SystemManager.is_mac_os():
            outpus = os.popen("osascript -e 'get volume settings'").readlines()[-1]
            sound_level = outpus.split(",")[0].split(":")[-1]
            return int(sound_level)
        else:
            return None

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
        else:
            return None

    # for use this command, need install https://github.com/nriley/brightness
    @staticmethod
    def brightness_level():
        if SystemManager.is_mac_os():
            outputs = os.popen("brightness -l").readlines()[1]
            brightness_level = int(float(outputs.split(" ")[-1]) * 100)
            return brightness_level
        else:
            return None

    # for use this command, need install https://github.com/nriley/brightness
    @staticmethod
    def set_brightness(value):
        if SystemManager.is_mac_os():
            command = f"brightness {value}"
            os.system(command)

    # for user this commnad, need install library: pynput
    @staticmethod
    def press_key(key):
        if SystemManager.is_mac_os():
            keyboard = Controller()

            Switch(key)\
                .case("prev", lambda: (keyboard.press(Key.media_previous), keyboard.release(Key.media_previous)))\
                .case("play", lambda: keyboard.press(Key.media_play_pause))\
                .case("next", lambda: (keyboard.press(Key.media_next), keyboard.release(Key.media_next)))\
                .case("left", lambda: keyboard.press(Key.left))\
                .case("space", lambda: keyboard.press(Key.space))\
                .case("right", lambda: keyboard.press(Key.right))

    @staticmethod
    def list_application():
        if SystemManager.is_mac_os():
            command = "osascript -e 'tell application \"System Events\" to get name of (processes where background only is false)'"
            outputs = os.popen(command).readlines()[-1].split(", ")
            applications = map(lambda application: str(application).replace("\n", ""), outputs)
            return list(applications)
        else:
            return None

    @staticmethod
    def close_application(application):
        if SystemManager.is_mac_os():
            command = f"pkill -9 {application}"
            os.system(command)
