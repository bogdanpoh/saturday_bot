from datetime import date
from models.currency import CurrencyItem
from services.course import CourseManager
from services.date import DateManager
from services.weather import WeatherManager
from services import download
from system.manager import SystemManager
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
        salary = CurrencyItem(
            name="Зарплата",
            value=constants.my_usd_salary,
            currency_name=constants.usd_name,
            type="sell"
        )
        apple_music = CurrencyItem(
            name="Підписка на Apple Music",
            value=constants.my_usd_apple_music_price,
            currency_name=constants.usd_name,
            type="buy"
        )
        my_euro = CurrencyItem(
            name="Збереження",
            value=constants.my_euros,
            currency_name=constants.euro_name,
            type="buy"
        )
        currencies_item = [salary, apple_music, my_euro]

        info = CourseManager.get_info(currencies_item=currencies_item)
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
        
    def weather(self, message):
        weather_manager = WeatherManager()
        weather = weather_manager.request()
        info = weather.info()
        image = download.fetch_image(weather.icon_url)
        self.bot.send_photo(message.chat.id, image, caption=info)
