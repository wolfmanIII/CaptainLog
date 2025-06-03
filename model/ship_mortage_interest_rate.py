from pyclbr import Class
from typing import TYPE_CHECKING
from typing import List
from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from model.base import Base

class ShipMortageInterestRate(Base):

    __tablename__ = "ship_mortgage_interest_rate"

    id: Mapped[int] = mapped_column(primary_key=True)
    duration: Mapped[int] = mapped_column(Integer)
    ship_price_multiplier: Mapped[int] = mapped_column(Numeric(11, 2))
    ship_price_divider: Mapped[int] = mapped_column(Integer)
    annual_interest_rate: Mapped[float] = mapped_column(Numeric(11, 2))



