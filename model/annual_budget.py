from typing import TYPE_CHECKING
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from model.base import Base
if TYPE_CHECKING:
    from model import ShipMortgage

class AnnualBudget(Base):
    __tablename__ = "annual_budget"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(36))
    start_day: Mapped[int] = mapped_column(Integer)
    end_day: Mapped[int] = mapped_column(Integer)
    start_year: Mapped[int] = mapped_column(Integer)
    end_year: Mapped[int] = mapped_column(Integer)
    ship_mortgage_id: Mapped[int] = mapped_column(ForeignKey("ship_mortgage.id"))
    ship_mortgage: Mapped["ShipMortgage"] = relationship(back_populates="annual_budgets")