from abc import ABC, abstractmethod
import pandas as pd
from wacc import WACC
from modeling import ProjectAssumptions

class BaseDCF(ABC):
    def __init__(self, company, forecast_years):
        self.company = company
        self.forecast_years = forecast_years
        self.terminal_growth_rate = 0.03
        self.dcf_table = None
        self.equity_value = None
        self.intrinsic_share_price = None
        self.wacc_model = WACC(self.company.ticker)
        self.assumptions = ProjectAssumptions(company.financial_data) 

    @abstractmethod
    def calculate_fcf(self):
        """Calculate Free Cash Flow (FCF) based on the specific method."""
        pass

    def calculate_dcf(self):
        projected_fcf = self.calculate_fcf()

        self.discount_rate = self.wacc_model.calculate_wacc()
        
        terminal_value = projected_fcf[-1] * (1 + self.terminal_growth_rate) / (self.discount_rate - self.terminal_growth_rate)
        discounted_fcf = self.discount_cash_flows(projected_fcf + [terminal_value])

        years = list(range(1, self.forecast_years + 1)) + ['Terminal Value']
        forecasted_fcf = projected_fcf + [terminal_value]

        self.dcf_table = pd.DataFrame({
            'Year': years,
            'Forecasted FCF ($)': forecasted_fcf,
            'Discounted FCF ($)': discounted_fcf
        })

    def discount_cash_flows(self, fcf_forecast):
        return [fcf / (1 + self.discount_rate) ** year for year, fcf in enumerate(fcf_forecast, start=1)]

    def calculate_equity_value(self):
        if self.dcf_table is None:
            raise ValueError("DCF Table is not calculated. Please run calculate_dcf() first.")
        total_dcf_value = self.dcf_table['Discounted FCF ($)'].sum()
        self.equity_value = total_dcf_value + self.company.cash - self.company.debt
        return self.equity_value

    def calculate_intrinsic_share_price(self):
        if self.equity_value is None:
            raise ValueError("Equity value is not calculated. Please run calculate_equity_value() first.")
        self.intrinsic_share_price = self.equity_value / self.company.shares_outstanding
        return self.intrinsic_share_price
