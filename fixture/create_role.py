from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from model import CrewRole

class Action():
    
    @staticmethod
    def create_role():
        engine = create_engine("sqlite:///captain_log.db", echo=True)

        with Session(engine) as session:
            role = CrewRole(
                code = "ENG",
                name = "Engineer",
                description = "Spaceship engineer"
            )
            session.add(role)
            session.commit()