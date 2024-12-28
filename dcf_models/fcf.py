from dcf_models.base import BaseDCF
from keys import FinStatement, FinKeys

class FreeCashFlowDCF(BaseDCF):
    """
    This class implements the discounted cash flow (DCF) valuation method using
    historical free cash flow (FCF) as a percentage of revenue. The formula used
    to calculate the free cash flow (FCF) is:

    FCF = Revenue * FCF Margin

    The FCF margin is calculated as the average historical FCF divided by revenue.

    The financial reasoning behind this approach is that FCF as a percentage of
    revenue is a good proxy for the company's ability to generate cash flow from
    its operations relative to its revenue. By projecting revenue and applying the
    FCF margin, we can estimate future FCFs for the DCF valuation.
    """
    def __init__(self, company, forecast_years):
        super().__init__(company, forecast_years)

    def calculate_fcf(self):
        # Calculate revenue growth rate based on historical data
        revenue_growth_rate = self.assumptions.calculate_growth_rate(statement=FinStatement.INCOME, key=FinKeys.REVENUE)
        
        # Get the latest revenue value
        revenue = self.company.get_latest_value(FinStatement.INCOME.value, FinKeys.REVENUE.value)
        
        # Get historical free cash flow (FCF) and calculate FCF margin
        fcf_data = self.company.get_data_range(FinStatement.CASHFLOW.value, FinKeys.FREE_CASH_FLOW.value)
        avg_fcf_margin = fcf_data.mean() / revenue if not fcf_data.empty else 0
        
        # Initialize a list to store projected FCF values
        projected_fcf = []
        
        # Project future FCF based on revenue growth and FCF margin
        for year in range(1, self.forecast_years + 1):
            revenue *= (1 + revenue_growth_rate) 
            fcf = revenue * avg_fcf_margin 
            projected_fcf.append(fcf)
        
        return projected_fcf