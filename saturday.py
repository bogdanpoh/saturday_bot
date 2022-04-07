import config
from telebot import TeleBot
from services.commands import CommandManager
from services.dialog import DialogManager
from helpers import constants
from helpers.switch import Switch

# for future
# from services.TimerManager import TimerManager
# from threading import Thread


bot = TeleBot(token=config.test_token)
command_manager = CommandManager(bot=bot)
dialog_manager = DialogManager(bot=bot)
currency_choose = None


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = str(call.data).split("_")[0]

    if data == "shortcut":
        dialog_manager.shortcuts_dialog(call)
    elif data == "key":
        dialog_manager.volume_dialog(call)
    else:
        dialog_manager.currencies_dialog(call)


@bot.message_handler(commands=constants.commands)
def command_handler(message):
    command = str(message.text).replace("/", "")

    Switch(command)\
        .case("course", lambda: command_manager.course(message=message))\
        .case("salary", lambda: command_manager.salary(message=message))\
        .case("currency", lambda: command_manager.currency(message=message))\
        .case("shortcuts", lambda: command_manager.shortcuts(message=message))\
        .case("volume", lambda: command_manager.volume(message=message))\
        .case("weather", lambda: command_manager.weather(message=message))


# def send_news():
#     date_manager = DateManager(date_from=date.today())
#
#     news = f"{date_manager.get_info()}\n\n"
#     news += f"{CourseManager.get_info()}"
#
#     bot.send_message(1, news)


def main():
    try:
        # check_message = Thread(target=TimerManager.check_event, args=("20:45:00", send_news))
        # check_message.start()
        print(f"{constants.bot_emoji} Saturday starting")

        bot.infinity_polling()
    except Exception as error:
        print(f"error: {error}")


if __name__ == "__main__":
    main()
