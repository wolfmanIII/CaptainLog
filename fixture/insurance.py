from sqlalchemy.orm import Session
from model.base import Base
from service.dblink import DBLink
from model.insurance import Insurance

def add_insurances():
    link = DBLink(echo=True)

    with Session(link.engine) as session:
        insurance_base = Insurance(
            name="Base",
            annual_cost=0.5,
            coverage=[
                "Collision damage",
                "Ship theft (not negligence)",
                "Structural failures"
            ]
        )
        session.add(insurance_base)

        insurance_extended = Insurance(
            name="Extended",
            annual_cost=1,
            coverage=[
                "Everything included in Base",
                "Piracy",
                "Space Anomalies",
                "Auto navigation errors",
            ]
        )
        session.add(insurance_extended)

        insurance_premium = Insurance(
            name="Premium",
            annual_cost=2,
            coverage=[
                "Everything included in Extended",
                "War zones",
                "Military actions",
                "Dangerous experiments",
                "Full refund in case of loss"
            ]
        )
        session.add(insurance_premium)

        session.commit()