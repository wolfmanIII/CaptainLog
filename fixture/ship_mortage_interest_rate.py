import ulid
from sqlalchemy.orm import Session
from model.base import Base
from service.dblink import DBLink
from model.ship_mortage_interest_rate import ShipMortageInterestRate

def add_rates():
    link = DBLink(echo=True)

    with Session(link.engine) as session:
        rate40 = ShipMortageInterestRate(
            duration = 40,
            ship_price_multiplier = 2,
            ship_price_divider = 240,
            annual_interest_rate = 1.75
        )
        session.add(rate40)

        rate30 = ShipMortageInterestRate(
            duration = 30,
            ship_price_multiplier = 1.75,
            ship_price_divider = 206,
            annual_interest_rate = 1.88
        )
        session.add(rate30)

        rate20 = ShipMortageInterestRate(
            duration = 20,
            ship_price_multiplier = 1.5,
            ship_price_divider = 160,
            annual_interest_rate = 2.05
        )
        session.add(rate20)

        rate10 = ShipMortageInterestRate(
            duration = 10,
            ship_price_multiplier = 1.25,
            ship_price_divider = 96,
            annual_interest_rate = 2.26
        )
        session.add(rate10)


        session.commit()