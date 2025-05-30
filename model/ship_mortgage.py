from typing import TYPE_CHECKING
from typing import List
from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from model.base import Base
if TYPE_CHECKING:
    from model import Ship, AnnualBudget

class ShipMortgage(Base):
    __tablename__ = "ship_mortgage"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(36))
    name: Mapped[str] = mapped_column(String(100))
    ship_id: Mapped[int] = mapped_column(ForeignKey("ship.id"))
    ship: Mapped["Ship"] = relationship(back_populates="ship_mortgage", single_parent=True)
    annual_budgets: Mapped[List["AnnualBudget"]] = relationship(back_populates="ship_mortgage")