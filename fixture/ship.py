import ulid
from sqlalchemy.orm import Session
from model.base import Base
from service.dblink import DBLink
from model.ship import Ship

def add_ships():
    link = DBLink(echo=True)

    with Session(link.engine) as session:
        ship = Ship(
            code=ulid.new().str,
            name="Lone Star",
            type="Far Trader",
            model = "Empress Marava",
            ship_price = 56000000
        )
        session.add(ship)

        session.commit()