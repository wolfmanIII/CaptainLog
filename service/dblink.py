from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///captain_log.db")
