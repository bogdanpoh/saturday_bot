from services.course import CourseManager
from system.manager import SystemManager
from helpers.keyboards import Keyboards
from helpers import constants


class DialogManager:
    currency_action = None
    currency = None

    def __init__(self, bot):
        self.bot = bot

    def shortcuts_dialog(self, call):
        shortcut = str(call.data).split("_")[-1]
        SystemManager.run_shortcut(shortcut)

        self.bot.answer_callback_query(call.id, f"{constants.bot_emoji} {shortcut}")

    def volume_dialog(self, call):
        value = str(call.data).split("_")[-1]
        SystemManager.set_volume(value)

        self.bot.answer_callback_query(call.id, f"{constants.bot_emoji} set volume: {value}")

    def currencies_dialog(self, call):
        course_manager = CourseManager()
        message = call.message
        text = None
        keyboard = Keyboards.buy_sell_keyboard()

        if call.data == Keyboards.callback_usd or call.data == Keyboards.callback_euro:
            currencies = course_manager.get_currencies(echo=True)

            if currencies:
                self.currency = currencies[0 if call.data == Keyboards.callback_usd else 1]
                text = CourseManager.format_currency(self.currency, new_line=False)
            else:
                text = f"{constants.currencies_choose} {constants.finger_down_emoji}"
                keyboard = Keyboards.currencies_keyboard()
                self.bot.answer_callback_query(call.id, f"{constants.currencies_too_many_requests} {constants.bot_emoji}")

        elif call.data == Keyboards.callback_back:
            text = f"{constants.currencies_choose} {constants.finger_down_emoji}"
            keyboard = Keyboards.currencies_keyboard()

        elif call.data == Keyboards.callback_buy or call.data == Keyboards.callback_sell:
            self.currency_action = Keyboards.callback_buy if call.data == Keyboards.callback_buy else Keyboards.callback_sell
            input_value = self.bot.send_message(message.chat.id, f"{constants.currency_enter_amount} {self.currency.emoji}:")
            self.bot.register_next_step_handler(input_value, self.process_get_value)
            return

        self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=keyboard)

    def process_get_value(self, message):
        try:
            calculated = 0
            action = ""
            uah_value = float(message.text)

            if self.currency_action == Keyboards.callback_buy:
                calculated = self.currency.buy(float(uah_value))
                action = constants.currency_buy
            elif self.currency_action == Keyboards.callback_sell:
                calculated = self.currency.sell(float(uah_value))
                action = constants.currency_sell

            text = f"{action} {self.currency.emoji} {uah_value} = {'%.2f' % calculated} UAH"
            self.bot.send_message(message.chat.id, text)

        except Exception as e:
            print(f"error: {e}")
            self.bot.reply_to(message, f'{constants.bot_emoji} ooops')
