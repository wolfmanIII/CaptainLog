from typing import TYPE_CHECKING
from typing import List
from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from model import Base
if TYPE_CHECKING:
    from model import ShipMortgage, Crew

class Ship(Base):
    __tablename__ = "ship"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(36))
    name: Mapped[str] = mapped_column(String(100))
    model: Mapped[str] = mapped_column(String(100))
    ship_price: Mapped[float] = mapped_column(Numeric(11, 2))
    ship_mortgage: Mapped["ShipMortgage"] = relationship(back_populates="ship")
    crew: Mapped[List["Crew"]] = relationship(back_populates="ship")