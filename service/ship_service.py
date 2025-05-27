from sqlalchemy import select
from model.ship import Ship
from service.dblink import DBLink


class ShipService():
    
    def get_all_ships(self):
        session = DBLink().getSession()
        stmt = select(Ship)
        return session.scalars(stmt)