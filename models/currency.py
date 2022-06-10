from models.base import BaseModel
from helpers import constants


class Currency(BaseModel):
    ccy = ""
    base_ccy = ""
    rate_buy = 0
    rate_sell = 0
    emoji = ""
    type = ""
    bank_name = ""

    def __init__(self, ccy, base_ccy, rate_buy, rate_sell, emoji, type, bank_name):
        self.ccy = ccy
        self.base_ccy = base_ccy
        self.rate_buy = round(rate_buy, 2)
        self.rate_sell = round(rate_sell, 2)
        self.emoji = emoji
        self.type = type
        self.bank_name = bank_name

    def buy(self, value):
        answer = round(float(value * self.rate_sell), 2)
        return answer

    def sell(self, value):
        answer = round(float(value * self.rate_buy), 2)
        return answer

    def info(self):
        return f"{self.emoji}\n{self.bank_name}\n{self.type}\n{constants.currency_buy}: {self.rate_buy}₴, {constants.currency_sell}: {self.rate_sell}₴"


class CurrencyItem(BaseModel):
    name = ""
    value = 0
    currency_name = None
    type = ""
    bank_name = ""

    def __init__(self, name, value, currency_name, type, bank_name):
        self.name = name
        self.value = value
        self.currency_name = currency_name
        self.type = type
        self.bank_name = bank_name

    def info(self, currency, new_line=False):
        symbol = "\n" if new_line else ""

        operation_value = currency.buy(self.value) if self.type == "buy" else currency.sell(self.value)
        return f"{self.name}: {self.value} {currency.emoji} = {operation_value} {constants.ukr_name} {symbol}"
