from typing import TYPE_CHECKING
from typing import List
from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from model.base import Base
if TYPE_CHECKING:
    from model import Ship, ShipRole

crew_ship_role_association_table = Table(
    "crew_ship_role",
    Base.metadata,
    Column("crew_id", ForeignKey("crew.id"), primary_key=True),
    Column("ship_role_id", ForeignKey("ship_role.id"), primary_key=True),
)
    
class Crew(Base):
    __tablename__ = "crew"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    surname: Mapped[str] = mapped_column(String(100))
    nickname: Mapped[str] = mapped_column(String(100), nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
    birth_year: Mapped[int] = mapped_column(Integer, nullable=True)
    birth_day: Mapped[int] = mapped_column(Integer, nullable=True)
    role: Mapped[List["ShipRole"]] = relationship(secondary=crew_ship_role_association_table)
    ship_id: Mapped[int] = mapped_column(ForeignKey("ship.id"), nullable=True)
    ship: Mapped["Ship"] = relationship(back_populates="crew")