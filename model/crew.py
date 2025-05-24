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
    from model import Ship, CrewRole

class Crew(Base):
    __tablename__ = "crew"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    surname: Mapped[str] = mapped_column(String(100))
    nickname: Mapped[str] = mapped_column(String(100), nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
    birth_year: Mapped[int] = mapped_column(Integer, nullable=True)
    birth_day: Mapped[int] = mapped_column(Integer, nullable=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("crew_role.id"), nullable=True)
    role: Mapped["CrewRole"] = relationship(back_populates="crew")
    ship_id: Mapped[int] = mapped_column(ForeignKey("ship.id"), nullable=True)
    ship: Mapped["Ship"] = relationship(back_populates="crew")