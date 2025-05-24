from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from model.base import Base

class DBLink:
    def __init__(self, echo: bool = False):
        self.engine = create_engine("sqlite:///captain_log.db", echo=echo)

    def close(self):
        Session(self.engine).close()
        
    def create_db(self):
        Base.metadata.create_all(self.engine)
        
    def drop_db(self):
        Base.metadata.drop_all(self.engine)