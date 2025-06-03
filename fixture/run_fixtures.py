from math import e
from operator import add
from model.base import Base
from model.ship import Ship
from service.dblink import DBLink
from model.ship_role import ShipRole
from sqlalchemy.orm import Session
from fixture.ship_role import add_ship_roles
from fixture.ship import add_ships
from fixture.ship_mortage_interest_rate import add_rates
import sys


def run(type):
    match type:
        case "create_db":
            link = DBLink(echo=True)
            link.create_db()
        case "ship_role":
            add_ship_roles()
        case "ship":
            add_ships()
        case "ship_mortgage_interest_rate":
            add_rates()

type = sys.argv[1]
run(type)

