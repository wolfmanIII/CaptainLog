from math import e
from operator import add
from model.base import Base
from model.ship import Ship
from service.dblink import DBLink
from model.ship_role import ShipRole
from sqlalchemy.orm import Session
from fixture.ship_role import add_ship_role

add_ship_role()