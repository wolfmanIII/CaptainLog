from typing import TYPE_CHECKING
from typing import List
from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from model.base import Base
if TYPE_CHECKING:
    from model import Ship, AnnualBudget, ShipMortageInterestRate

class ShipMortgage(Base):
    __tablename__ = "ship_mortgage"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(36))
    name: Mapped[str] = mapped_column(String(100))
    ship_id: Mapped[int] = mapped_column(ForeignKey(name="fk_ship_id", column="ship.id"))
    ship: Mapped["Ship"] = relationship(back_populates="ship_mortgage", single_parent=True)
    rate_id: Mapped[int] = mapped_column(ForeignKey(name="fk_ship_mortagage_interest_rate_id", column="ship_mortgage_interest_rate.id"))
    rate: Mapped["ShipMortageInterestRate"] = relationship(back_populates="ship_mortgage", single_parent=True)
    start_day: Mapped[int] = mapped_column(Integer)
    start_year: Mapped[int] = mapped_column(Integer)
    ship_shares: Mapped[int] = mapped_column(Integer, nullable=True)
    advance_payment: Mapped[float] = mapped_column(Numeric(11, 2), nullable=True)
    discount: Mapped[float] = mapped_column(Numeric(11, 2), nullable=True)
    annual_budgets: Mapped[List["AnnualBudget"]] = relationship(back_populates="ship_mortgage")