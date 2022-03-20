from models.base import BaseModel


class Currency(BaseModel):
    ccy = ""
    base_ccy = ""
    rate_buy = 0
    rate_sell = 0
    emoji = ""

    def __init__(self, ccy, base_ccy, rate_buy, rate_sell, emoji):
        self.ccy = ccy
        self.base_ccy = base_ccy
        self.rate_buy = round(rate_buy, 2)
        self.rate_sell = round(rate_sell, 2)
        self.emoji = emoji

    def buy(self, value):
        answer = round(float(value * self.rate_sell), 2)
        return answer

    def sell(self, value):
        answer = round(float(value * self.rate_buy), 2)
        return answer


class CurrencyItem(BaseModel):
    name = ""
    value = 0
    currency_name = None

    def __init__(self, name, value, currency_name):
        self.name = name
        self.value = value
        self.currency_name = currency_name

    def info(self, currency, new_line=False):
        symbol = "\n" if new_line else ""
        return f"{self.name}: {self.value} {currency.emoji} = {currency.buy(self.value)} UAH {symbol}"
