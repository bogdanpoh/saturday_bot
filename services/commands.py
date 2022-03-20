from datetime import date
from services.course import CourseManager
from services.date import DateManager
from system.system_manager import SystemManager
from helpers.keyboards import Keyboards
from helpers import constants


class CommandManager(object):

    def __init__(self, bot):
        self.bot = bot

    def send_message(self, message, text, keyboard=None):
        if keyboard:
            self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
        else:
            self.bot.send_message(message.chat.id, text)

    def course(self, message):
        info = CourseManager.get_info()
        self.send_message(message, info)

    def salary(self, message):
        use_dev_locale = SystemManager.is_mac_os()
        date_manager = DateManager(date_from=date.today(), dev_locale=use_dev_locale)
        currencies_info = date_manager.get_info()

        self.send_message(message, currencies_info)

    def currency(self, message):
        text = f"{constants.currencies_choose} {constants.finger_down_emoji}"
        self.send_message(message=message, text=text, keyboard=Keyboards.currencies_keyboard())

    def shortcuts(self, message):
        text = ""
        keyboard = None
        shortcuts = SystemManager.list_shortcuts()

        if shortcuts:
            text = "Shortcuts"
            keyboard = Keyboards.shortcuts_keyboard(shortcuts)
        else:
            text = f"{constants.bot_emoji} This is don't MacOS"

        self.send_message(message=message, text=text, keyboard=keyboard)

    def volume(self, message):
        text = ""
        keyboard = None

        if SystemManager.is_mac_os():
            text = "Volume"
            keyboard = Keyboards.volume_keyboard()
        else:
            text = f"{constants.bot_emoji} This is don't MacOS"

        self.send_message(message=message, text=text, keyboard=keyboard)