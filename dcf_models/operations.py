from dcf_models.base import BaseDCF
from keys import FinStatement, FinKeys

class CashFlowOperationsDCF(BaseDCF):
    """
    This class implements the discounted cash flow (DCF) valuation method using
    cash flow from operations as the cash flow proxy. It adjusts for interest expense, 
    tax shield, and capital expenditures (CAPEX).
    """
    def __init__(self, company, forecast_years):
        super().__init__(company, forecast_years)

    def calculate_fcf(self):
        # Calculate growth rates using the assumptions, handle missing keys
        try:
            
            cfo_growth_rate = self.assumptions.calculate_growth_rate(statement=FinStatement.CASHFLOW, key=FinKeys.CASH_FLOW_OPERATIONS)
            capex_growth_rate = self.assumptions.calculate_growth_rate(statement=FinStatement.CASHFLOW, key=FinKeys.CAPEX)
        except KeyError:
            cfo_growth_rate = 0  # Default to 0 growth if missing
            capex_growth_rate = 0

        # Get latest values, handle missing values gracefully
        cfo = self.company.get_latest_value(FinStatement.CASHFLOW.value, FinKeys.CASH_FLOW_OPERATIONS.value) or 0
        interest_expense = self.company.get_latest_value(FinStatement.INCOME.value, FinKeys.INTEREST_EXPENSE.value) or 0
        capex = abs(self.company.get_latest_value(FinStatement.CASHFLOW.value, FinKeys.CAPEX.value) or 0)
        tax_provision = self.company.get_latest_value(FinStatement.INCOME.value, FinKeys.TAX_PROVISION.value) or 0
        pretax_income = self.company.get_latest_value(FinStatement.INCOME.value, FinKeys.PRETAX_INCOME.value) or 0

        tax_rate = tax_provision / pretax_income if pretax_income != 0 else 0

        # Calculate the initial interest expense to CFO ratio
        interest_to_cfo_ratio = interest_expense / cfo if cfo != 0 else 0

        projected_fcf = []
        for year in range(1, self.forecast_years + 1):
            # Project values for the year
            cfo *= (1 + cfo_growth_rate)
            capex *= (1 + capex_growth_rate)
            
            # Calculate interest expense based on the constant ratio to CFO
            interest_expense = cfo * interest_to_cfo_ratio
            
            # Calculate FCFF
            fcf = cfo + interest_expense * (1 - tax_rate) - capex
            projected_fcf.append(fcf)
            
        return projected_fcf
