from model.crew import Crew
from service.dblink import DBLink


class CrewService():
    
    def get_all_crew(self):
        session = DBLink().getSession()
        return session.query(Crew).all()