import requests

import config
from helpers import constants
from models.currency import Currency, CurrencyItem


class CourseManager(object):

    @staticmethod
    def format_code_currency(code):
        for key, value in constants.currencies_name.items():
            if key == code:
                return value
        return None

    @staticmethod
    def format_emoji_currency(name):
        for key, value in constants.currencies_emoji.items():
            if key == name:
                return value
        return None

    @staticmethod
    def fetch_currency(data):

        ccy = CourseManager.format_code_currency(data["currencyCodeA"])
        base_ccy = CourseManager.format_code_currency(data["currencyCodeB"])
        rate_buy = float(data["rateBuy"])
        rate_sell = float(data["rateSell"])
        emoji = CourseManager.format_emoji_currency(ccy)

        return Currency(
            ccy=ccy,
            base_ccy=base_ccy,
            rate_buy=rate_buy,
            rate_sell=rate_sell,
            emoji=emoji
        )

    @staticmethod
    def get_currencies(echo=False):
        response = requests.get(url=constants.currencies_url, verify=False)

        if echo:
            print(f"status code: {response.status_code}")
            print(f"response: {response.json()}")

        if response.status_code == 200:
            currencies = []
            data = response.json()

            for index, item in enumerate(data):
                if index <= 1:
                    currency = CourseManager.fetch_currency(data[index])
                    currencies.append(currency)

            return currencies
        else:
            return None

    @staticmethod
    def format_currency(currency, new_line=False):
        emoji = currency.emoji
        buy = currency.rate_buy
        sell = currency.rate_sell
        symbol = '\n' if new_line else ' '

        return f"{emoji}{symbol}{constants.currency_sell}: {sell}₴, {constants.currency_buy}: {buy}₴\n"

    @staticmethod
    def get_info():
        info = ""
        currencies = CourseManager.get_currencies(echo=config.echo)

        if currencies:
            usd = [currency for currency in currencies if currency.ccy == "USD"][0]
            euro = [currency for currency in currencies if currency.ccy == "EUR"][0]

            salary = CurrencyItem(name="Зарплата", value=constants.my_usd_salary, currency=usd)
            apple_music = CurrencyItem(name="Підписка на Apple Music", value=constants.my_usd_apple_music_price,
                                       currency=usd)
            my_euro = CurrencyItem(name="Збереження", value=constants.my_euros, currency=euro)

            info += CourseManager.format_currency(usd, new_line=True)
            info += salary.info(new_line=True)
            info += apple_music.info(new_line=True)
            info += "\n" + CourseManager.format_currency(euro, new_line=True)
            info += my_euro.info()
        else:
            info = f"{constants.currencies_too_many_requests} {constants.bot_emoji}"

        return info
