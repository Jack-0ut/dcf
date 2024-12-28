from dcf_models.base import BaseDCF
from keys import FinStatement, FinKeys

class NopatDCF(BaseDCF):
    """
    This class implements the discounted cash flow (DCF) valuation method using
    net operating profit after taxes (NOPAT) as the cash flow proxy.
    NOPAT = Operating Income * (1 - Tax Rate) or NOPAT = EBIT * (1 - Tax Rate)
    We use the operating margin as our proxy for the cash flow.
    """
    def __init__(self, company, forecast_years):
        super().__init__(company, forecast_years)

    def calculate_fcf(self):
        # Calculate growth rates using the assumptions
        revenue_growth_rate = self.assumptions.calculate_growth_rate(statement=FinStatement.INCOME, key=FinKeys.REVENUE)
        capex_growth_rate = self.assumptions.calculate_growth_rate(statement=FinStatement.CASHFLOW, key=FinKeys.CAPEX)
        wc_growth_rate = self.assumptions.calculate_growth_rate(statement=FinStatement.CASHFLOW, key=FinKeys.CHANGE_IN_WORKING_CAPITAL)

        revenue = self.company.get_latest_value(FinStatement.INCOME.value, FinKeys.REVENUE.value)
        operating_income = self.company.get_latest_value(FinStatement.INCOME.value, FinKeys.OPERATING_INCOME.value)
        operating_margin = operating_income / revenue
        tax_provision = self.company.get_latest_value(FinStatement.INCOME.value, FinKeys.TAX_PROVISION.value)
        pretax_income = self.company.get_latest_value(FinStatement.INCOME.value, FinKeys.PRETAX_INCOME.value)
        tax_rate = tax_provision / pretax_income if pretax_income != 0 else 0

        # Historical data for averages
        depreciation_data = self.company.get_data_range(FinStatement.CASHFLOW.value, FinKeys.DEPRECIATION.value)
        capex_data = self.company.get_data_range(FinStatement.CASHFLOW.value, FinKeys.CAPEX.value)
        change_in_working_capital_data = self.company.get_data_range(FinStatement.CASHFLOW.value, FinKeys.CHANGE_IN_WORKING_CAPITAL.value)

        avg_depreciation = depreciation_data.mean() if not depreciation_data.empty else 0
        avg_capex = abs(capex_data.mean()) if not capex_data.empty else 0
        avg_change_in_wc = change_in_working_capital_data.mean() if not change_in_working_capital_data.empty else 0

        # Initial calculations for NOPAT and FCF
        capex_to_revenue_ratio = avg_capex / revenue
        nopat = operating_income * (1 - tax_rate)
        fcf = nopat - avg_capex + avg_depreciation - avg_change_in_wc

        projected_fcf = []
        for year in range(1, self.forecast_years + 1):
            revenue *= (1 + revenue_growth_rate)
            operating_income = revenue * operating_margin
            nopat = operating_income * (1 - tax_rate)
            
            capex = revenue * capex_to_revenue_ratio * (1 + capex_growth_rate)
            change_in_wc = avg_change_in_wc * (1 + wc_growth_rate)
            depreciation = revenue * (avg_depreciation / revenue)
            
            fcf = nopat + depreciation - capex - change_in_wc
            projected_fcf.append(fcf)

        return projected_fcf