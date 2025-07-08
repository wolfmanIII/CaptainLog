from model.annual_budget import AnnualBudget
from service.dblink import DBLink


class AnnualBudgetService():
    
    def get_all_budgets(self):
        session = DBLink().getSession()
        return session.query(AnnualBudget).all()