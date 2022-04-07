from models.base import BaseModel
import math


class Currency(BaseModel):
    ccy = ""
    base_ccy = ""
    rate_buy = 0
    rate_sell = 0
    emoji = ""

    @staticmethod
    def round_half_up(n, decimals=0) -> float:
        multiplier = 10 ** decimals
        return math.floor(n * multiplier + 0.5) / multiplier

    def __init__(self, ccy, base_ccy, rate_buy, rate_sell, emoji):
        self.ccy = ccy
        self.base_ccy = base_ccy
        self.rate_buy = rate_buy
        self.rate_sell = rate_sell
        self.emoji = emoji

    def rate_buy_short(self) -> float:
        return Currency.round_half_up(self.rate_buy, 2)

    def rate_sell_short(self) -> float:
        return Currency.round_half_up(self.rate_sell, 2)

    def buy(self, value) -> float:
        float_value = float(value) * self.rate_sell
        return float_value

    def sell(self, value) -> float:
        float_value = float(value) * self.rate_buy
        return float_value


class CurrencyItem(BaseModel):
    name = ""
    value = 0
    currency_name = None
    type = ""

    def __init__(self, name, value, currency_name, type):
        self.name = name
        self.value = value
        self.currency_name = currency_name
        self.type = type

    def info(self, currency, new_line=False):
        symbol = "\n" if new_line else ""
        value = currency.buy(self.value) if type == "buy" else currency.sell(self.value)
        money = Currency.round_half_up(value, 2)
        return f"{self.name}: {self.value} {currency.emoji} = {money} UAH {symbol}"
