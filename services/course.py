import requests
import config
from helpers import constants
from models.currency import Currency


class CourseManager(object):

    @staticmethod
    def format_code_currency(code):
        for key, value in constants.currencies_code_name.items():
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
            print(f"response:")
            print(response.json())

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
        buy = currency.rate_buy_short()
        sell = currency.rate_sell_short()
        symbol = "\n" if new_line else " "

        return f"{emoji}{symbol}{constants.currency_sell}: {sell}₴, {constants.currency_buy}: {buy}₴\n"

    @staticmethod
    def get_info(currencies_item):
        info = ""
        currencies = CourseManager.get_currencies(echo=config.echo)

        if currencies:
            for currency in currencies:
                info += CourseManager.format_currency(currency, new_line=True)
                sorted_currencies_item = [item for item in currencies_item if item.currency_name == currency.ccy]

                for item in sorted_currencies_item:
                    info += item.info(currency=currency, new_line=True)

                info += "\n"
        else:
            info = f"{constants.currencies_too_many_requests} {constants.bot_emoji}"

        return info
