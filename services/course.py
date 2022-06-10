import requests
import config
from helpers import constants
from models.currency import Currency, CurrencyItem


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
    def get_mono_currencies(echo=False):
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
                    course = data[index]
                    ccy = CourseManager.format_code_currency(course["currencyCodeA"])
                    base_ccy = CourseManager.format_code_currency(course["currencyCodeB"])
                    rate_buy = float(course["rateBuy"])
                    rate_sell = float(course["rateSell"])
                    emoji = CourseManager.format_emoji_currency(ccy)

                    currency = Currency(
                        ccy=ccy,
                        base_ccy=base_ccy,
                        rate_buy=rate_buy,
                        rate_sell=rate_sell,
                        emoji=emoji,
                        type=constants.curreny_onlie,
                        bank_name=constants.mono_name
                    )
                    currencies.append(currency)

            return currencies
        else:
            return None

    @staticmethod
    def get_private_currencies(echo=False) -> [Currency]:
        response = requests.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")

        if echo:
            print(f"status code: {response.status_code}")
            print(f"response:")
            print(response.json())

        if response.status_code == 200:
            currencies = []
            usd_currency_data = response.json()[0]
            emoji = CourseManager.format_emoji_currency(usd_currency_data["ccy"])

            usd_currency = Currency(
                ccy=usd_currency_data["ccy"],
                base_ccy=usd_currency_data["base_ccy"],
                rate_buy=float(usd_currency_data["buy"]),
                rate_sell=float(usd_currency_data["sale"]),
                emoji=emoji,
                type=constants.curreny_departament,
                bank_name=constants.privatbank_name
            )
            currencies.append(usd_currency)
            return currencies
        else:
            return None

    @staticmethod
    def get_alfa_currencies(echo=False) -> [Currency]:
        response = requests.get("https://alfabank.ua/currency-exchange")

        if echo:
            print(f"status code: {response.status_code}")
            print(f"response:")
            print(response.json())

        if response.status_code == 200:
            currencies = []
            emoji = CourseManager.format_emoji_currency(constants.usd_name)
            text = str(response.text)
            start_index = text.find("department:[{label:U")
            text_with_course = text[start_index: start_index + 100]
            array_with_course = text_with_course.split("\"")

            usd_buy = float(array_with_course[1])
            usd_sell = float(array_with_course[3])
            usd_currency = Currency(
                constants.usd_name,
                base_ccy=constants.ukr_name,
                rate_buy=usd_buy,
                rate_sell=usd_sell,
                emoji=emoji,
                type=constants.curreny_departament,
                bank_name=constants.alfabank_name
            )
            currencies.append(usd_currency)

            return currencies
        else:
            return None

    @staticmethod
    def format_currency(currency, new_line=False):
        emoji = currency.emoji
        buy = currency.rate_buy
        sell = currency.rate_sell
        symbol = f"\n{currency.bank_name}\n{currency.type}\n" if new_line else f"\n{currency.bank_name}\n{currency.type} "

        return f"{emoji}{symbol}{constants.currency_sell}: {sell}₴, {constants.currency_buy}: {buy}₴\n"

    @staticmethod
    def get_item_info(currency, currencies_item: [CurrencyItem]) -> str:
        info = ""

        for item in currencies_item:
            if currency.ccy == item.currency_name:
                info += item.info(currency, new_line=True)

        return info

    @staticmethod
    def get_info(currencies_item: [CurrencyItem]):
        info = ""
        currencies = []
        mono_currencies = CourseManager.get_mono_currencies(echo=config.echo)
        # alfa_currencies = CourseManager.get_alfa_currencies(echo=config.echo)
        privat_currencies = CourseManager.get_private_currencies(echo=config.echo)

        if mono_currencies:
            for currency in mono_currencies:
                currencies.append(currency)

        # for currency in alfa_currencies:
        #     currencies.append(currency)

        for currency in privat_currencies:
            currencies.append(currency)

        for currency in currencies:
            usd_info = currency.info()
            info += f"{usd_info}\n\n"

            sorted_currencies_item = [item for item in currencies_item if item.bank_name == currency.bank_name and item.currency_name == currency.ccy]
            info += CourseManager.get_item_info(currency, sorted_currencies_item) + "\n"

        return info
