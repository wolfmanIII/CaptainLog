from typing import List
from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass