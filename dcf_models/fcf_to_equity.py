from dcf_models.base import BaseDCF
from keys import FinStatement, FinKeys

class FreeCashFlowToEquity(BaseDCF):
    def __init__(self, company, forecast_years):
        super().__init__(company, forecast_years)
    
    def calculate_fcf(self):
        raise NotImplementedError