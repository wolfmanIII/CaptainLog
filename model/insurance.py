from typing import TYPE_CHECKING
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from model.base import Base
from util.string_list import StringList
if TYPE_CHECKING:
    from model.ship_mortgage import ShipMortgage

class Insurance(Base):

    __tablename__ = "insurance"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    annual_cost: Mapped[float] = mapped_column(Numeric(11, 2))
    coverage: Mapped[list[str]] = mapped_column(StringList)
    ship_mortgage: Mapped["ShipMortgage"] = relationship(back_populates="insurance")