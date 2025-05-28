from model.ship import Ship
from service.dblink import DBLink


class ShipService():
    
    def get_all_ships(self):
        session = DBLink().getSession()
        return session.query(Ship).all()