from system.manager import SystemManager


class ServerCommands(object):

    @staticmethod
    def list_shortcuts():
        list_shortcuts = SystemManager.list_shortcuts()

        if list_shortcuts:
            response = {"count": len(list_shortcuts), "shortcuts": list_shortcuts}
            return response
        else:
            return None

    @staticmethod
    def run_shortcut(shortcut):
        SystemManager.run_shortcut(shortcut)

    @staticmethod
    def system():
        device_name = SystemManager.device_name()
        battery_charg = SystemManager.battery_charg()
        sound_level = SystemManager.sound_level()
        brightness_level = SystemManager.brightness_level()

        if device_name and battery_charg and sound_level and brightness_level:
            response = {
                "device_name": device_name,
                "battery_charg": battery_charg,
                "sound_level": sound_level,
                "brightness_level": brightness_level
            }
            return response
        else:
            return None

    @staticmethod
    def set_volume(value):
        SystemManager.set_volume(value)

    @staticmethod
    def set_brightness(value):
        SystemManager.set_brightness(value)

    @staticmethod
    def press_key(key):
        SystemManager.press_key(key)

    @staticmethod
    def list_applications():
        applications = SystemManager.list_application()

        if applications:
            response = {"count": len(applications), "applications": applications}
            return response
        else:
            return None

    @staticmethod
    def close_application(application):
        SystemManager.close_application(application)
