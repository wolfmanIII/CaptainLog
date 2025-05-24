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
    from model import Crew

class ShipRole(Base):
    __tablename__ = "ship_role"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(4))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000))