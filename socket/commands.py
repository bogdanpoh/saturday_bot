import socket
import json
from system.manager import SystemManager


class ServerCommands(object):

    # def __init__(self, connection: socket, address: str):
    #     self.socket = connection
    #     self.address = address

    # def send(self, data):
    #     self.socket.sendto(bytes(data, encoding="utf-8"), self.address)

    @staticmethod
    def list_shortcuts():
        list_shortcuts = list(SystemManager.list_shortcuts())
        response = {
            "count": len(list_shortcuts),
            "shortcuts": list_shortcuts
        }

        # data_response = json.dumps(response)
        # self.send(data_response)
        return response

    @staticmethod
    def run_shortcut(shortcut):
        SystemManager.run_shortcut(shortcut)

    @staticmethod
    def system():
        device_name = SystemManager.device_name()
        battery_charg = SystemManager.battery_charg()
        sound_level = SystemManager.sound_level()
        brightness_level = SystemManager.brightness_level()
        response = {
            "device_name": device_name,
            "battery_charg": battery_charg,
            "sound_level": sound_level,
            "brightness_level": brightness_level
        }

        # data_response = json.dumps(response)
        # self.send(response)
        return response

    @staticmethod
    def set_volume(value):
        SystemManager.set_volume(value)

    @staticmethod
    def set_brightness(value):
        SystemManager.set_brightness(value)

    @staticmethod
    def press_key(key):
        SystemManager.press_key(key)
