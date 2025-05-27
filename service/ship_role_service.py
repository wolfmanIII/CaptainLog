from sqlalchemy import select
from model.ship_role import ShipRole
from service.dblink import DBLink


class ShipRoleService():
    
    def get_all_ship_roles(self):
        session = DBLink().getSession()
        stmt = select(ShipRole)
        return session.scalars(stmt)