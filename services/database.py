from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import date
# from models.CurrencyEntity import CurrencyEntity
from helpers import constants

Base = declarative_base()
engine = create_engine("sqlite:///saturday_database.db", echo=False)
Session = sessionmaker(bind=engine)


class CurrencyEntity(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True)
    ccy = Column(String)
    base_ccy = Column(String)
    buy = Column(Float)
    sell = Column(Float)
    date = Column(String)

    def __init__(self, ccy, base_ccy, buy, sell, date):
        self.ccy = ccy
        self.base_ccy = base_ccy
        self.buy = buy
        self.sell = sell
        self.date = date

    @classmethod
    def from_currency(self, currency, date):
        return self(ccy=currency.ccy, base_ccy=currency.base_ccy, buy=currency.rate_buy, sell=currency.rate_sell, date=date)

    def __repr__(self):
        return f"{self.__class__.__name__} #{self.id}"

    def __str__(self):
        return f"ccy: {self.ccy} base_ccy: {self.base_ccy} buy: {self.buy} sell: {self.sell} date: {self.date}"


class DatabaseManager(object):
    # Base = declarative_base()

    def __init__(self):
        Base.metadata.create_all(engine)

    def save(self, entity):
        with Session() as session:
                session.add(entity)
                session.commit()

    def get_by_date(self, enitity, date):
        with Session() as session:
            return session.query(enitity).filter(enitity.date == date).all()

    def get_by_ccy(self, enitity, ccy):
        with Session() as session:
            currency = session.query(enitity).filter(enitity.ccy == ccy).first()
            return currency

    def update_currency_by_id(self, id, buy=None, sell=None, date=None):
        with Session() as session:
            currency = session.query(CurrencyEntity).get(id)

            if buy:
                currency.buy = buy
            if sell:
                currency.sell = sell
            if date:
                currency.date = date

            session.commit()
            return session.query(CurrencyEntity).get(id)

    def remove_by_date(self, enitity, date):
        with Session() as session:
            session.query(enitity).filter(enitity.date == date).delete()
            session.commit()

    def remove_by_id(self, id):
        with Session() as session:
            session.query(CurrencyEntity).get(id).delete()
            session.commit()


# class PhotoModel(Base):
#     __tablename__ = "photo"
#     id = Column(Integer, primary_key=True)
#     url = Column(String)
#
#     def __init__(self, url):
#         self.url = url
#
#     def __repr__(self):
#         return f"{self.__class__.__name__} #{self.id}"
#
#
# class TagModel(Base):
#     __tablename__ = "tag"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#
#     def __init__(self, name):
#         self.name = name
#
#     def __repr__(self):
#         return f"{self.__class__.__name__} #{self.id}"
#
#     def get_photos(self) -> Query:
#         with Session() as session:
#             return (
#                 session.query(PhotoModel, TagModel)
#                 .with_entities(PhotoModel)
#                 .filter(PhotoModel.id == self.id)
#             )


# def fill_data():
#     current_date = date.today()
#     usd = Currency(ccy="USD", base_ccy="UAH", buy="30.25", sell="29.20", date=current_date)
#     euro = Currency(ccy="EURO", base_ccy="UAH", buy="11.11", sell="12.12", date=current_date)
#
#     with Session() as session:
#         session.add(usd)
#         session.add(euro)
#         session.commit()


def main():
    # fill_data()

    # with Session() as session:
    # update()
    # removeWithDate(current_date)
    # currencies = session.query(Currency).filter(Currency.date == current_date)

    # for currency in get_by_date(current_date):
    #     print(str(currency))

    # euro = get_by_ccy("EURO")
    # update_by_id(euro.id, buy=11.11)

    # usd = get_by_ccy("USD")
    # update_usd = update_by_id(usd.id, sell=29.2)
    # print(update_usd)

    # euro = get_by_ccy("EURO")
    # euro_date = euro.date

    # print(datea)

    database_manager = DatabaseManager()
    current_date = date.today().strftime(constants.date_format)

    # for currency in database_manager.get_by_date(CurrencyEntity, current_date):
    #     print(currency)

    # database_manager.remove_by_date(CurrencyEntity, current_date)

    # for currency in database_manager.get_by_date(CurrencyEntity, current_date):
    #     print(currency)

    # usd = CurrencyEntity(ccy="USD", base_ccy="UAH", buy="30.25", sell="29.20", date=current_date)
    # database_manager.save(usd)


if __name__ == '__main__':
    main()

