from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from helpers import constants


class Keyboards(object):
    callback_usd = "callback_button_usd"
    callback_euro = "callback_button_euro"
    callback_buy = "callback_button_buy"
    callback_sell = "callback_button_sell"
    callback_back = "callback_button_back"

    @staticmethod
    def currencies_keyboard() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(
            InlineKeyboardButton(
                f"{constants.usd_name} {constants.currencies_emoji[f'{constants.usd_name}']}",
                callback_data=Keyboards.callback_usd
            ),
            InlineKeyboardButton(
                f"{constants.euro_name} {constants.currencies_emoji[f'{constants.euro_name}']}",
                callback_data=Keyboards.callback_euro
            )
        )

        return markup

    @staticmethod
    def buy_sell_keyboard() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(
            InlineKeyboardButton(f"{constants.currency_buy}", callback_data=Keyboards.callback_buy),
            InlineKeyboardButton(f"{constants.currency_sell}", callback_data=Keyboards.callback_sell),
            InlineKeyboardButton(f"{constants.back} {constants.arrow_left_emoji}",
                                 callback_data=Keyboards.callback_back)
        )

        return markup

    @staticmethod
    def shortcuts_keyboard(shortcuts) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        shortcut_bottons = (InlineKeyboardButton(f"{shortcut}", callback_data=f"shortcut_{shortcut}") for shortcut in
                            shortcuts)

        for button in shortcut_bottons:
            markup.add(button)

        return markup

    @staticmethod
    def volume_keyboard() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.row_width = 2

        decimal_numbers = [float(number) for number in range(0, 11)]
        float_numbers = [number + 0.5 for number in decimal_numbers]

        for number in decimal_numbers:
            index = decimal_numbers.index(number)

            if float_numbers[index] <= 10:
                markup.add(
                    InlineKeyboardButton(number, callback_data=f"key_{number}"),
                    InlineKeyboardButton(float_numbers[index], callback_data=f"key_{float_numbers[index]}")
                )

        markup.add(InlineKeyboardButton(decimal_numbers[-1], callback_data=f"key_{decimal_numbers[-1]}"))
        return markup
