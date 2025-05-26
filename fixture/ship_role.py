from sqlalchemy.orm import Session
from model.base import Base
from service.dblink import DBLink
from model.ship_role import ShipRole

def add_ship_roles():
    link = DBLink(echo=True)

    # Create ship roles in the database
    with Session(link.engine) as session:
        ship_role = ShipRole(
            code="CAP",
            name="Captain",
            description="Spaceship captain"
        )
        session.add(ship_role)
        
        ship_role = ShipRole(
            code="ENG",
            name="Engineer",
            description="Spaceship engineer"
        )
        session.add(ship_role)
        
        ship_role = ShipRole(
            code="PIL",
            name="Pilot",
            description="Spaceship pilot"
        )
        session.add(ship_role)
        
        ship_role = ShipRole(
            code="NAV",
            name="Navigator",
            description="Spaceship navigator"
        )
        session.add(ship_role)
        
        ship_role = ShipRole(
            code="SCI",
            name="Scientist",
            description="Spaceship scientist"
        )
        session.add(ship_role)
        
        ship_role = ShipRole(
            code="MED",
            name="Medic",
            description="Spaceship medic"
        )
        session.add(ship_role)
        
        ship_role = ShipRole(
            code="MAR",
            name="Marine",
            description="Spaceship marine"
        )
        session.add(ship_role)
        
        ship_role = ShipRole(
            code="TEC",
            name="Technician",
            description="Spaceship technician"
        )
        session.add(ship_role)
        
        session.commit()