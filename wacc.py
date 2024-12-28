import yfinance as yf 
class WACC:
    """
    The WACC class calculates the Weighted Average Cost of Capital (WACC) for a given stock ticker.

    Attributes:
        ticker (str): The stock ticker symbol (e.g. "AAPL")
    """

    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

        self.market_bond_spread = 0.02
        self.risk_free_rate = self.get_risk_free_rate()
        self.market_return = self.get_historical_market_return()
        self.beta = self.stock.info.get('beta', 1) 
        self.equity_value = self.stock.info.get('marketCap', 0)  
        self.debt_value = self.get_debt_value()
        self.tax_rate = self.calculate_effective_tax_rate()

        print("##### Calculating WACC #####")
        print(f"Risk-free rate: {self.risk_free_rate:.2%}")
        print(f"Beta: {self.beta}")
        print(f"Market Return: {self.market_return:.2%}")

    def get_debt_value(self):
        """
        Retrieves the total debt value from the company's balance sheet.

        Returns:
            float: The total debt value
        """
        balance_sheet = self.stock.balance_sheet
        total_debt = balance_sheet.loc['Total Debt']
        return total_debt.iloc[0] if not total_debt.empty else 0
    
    def get_risk_free_rate(self):
        """
        Returns the 10-year Treasury yield as a proxy for the risk-free rate.

        Returns:
            float: The risk-free rate
        """
        treasury_data = yf.Ticker("^TNX")  # 10-year Treasury yield
        periods = ['1d', '5d', '1mo', '3mo']
        for period in periods:
            try:
                return treasury_data.history(period=period)['Close'].iloc[-1] / 100
            except IndexError:
                pass
        raise ValueError("No risk free rate data available")  

    def get_historical_market_return(self,ticker="^GSPC"):
        """
        Calculates the average historical return of a given index.
        By default, it uses the S&P 500 Index (^GSPC), but other indices can be specified.

        Args:
            ticker (str): The ticker symbol of the index. Defaults to "^GSPC".
                Example values: "^GSPC" (S&P 500 Price Index), 
                "^SP500TR" (S&P 500 Total Return Index), 
                "^DWCF" (Dow Jones Total Stock Market Index).
                "^RUA" (Russell 3000 Index),
                "^FTW5000" (Wilshare 5000 Public Trading US Companies Index).

        Returns:
            float: The historical market return
        """
        index = yf.Ticker(ticker)
        historical_data = index.history(period="max")
        
        # Ensure that the 'Close' column is available
        if 'Close' not in historical_data.columns:
            raise ValueError("The selected ticker does not contain 'Close' data.")
        
        historical_data['Year'] = historical_data.index.year
        yearly_returns = historical_data['Close'].resample('YE').ffill().pct_change().dropna()

        average_return = yearly_returns.mean()
        
        return average_return
    def calculate_effective_tax_rate(self):
        """
        Calculates the effective tax rate based on the company's income statement data.

        Returns:
            float: The effective tax rate
        """
        income_statement = self.stock.financials.T

        if 'Tax Provision' in income_statement.columns and 'Pretax Income' in income_statement.columns:
            tax_provision = income_statement['Tax Provision'].iloc[0]
            pretax_income = income_statement['Pretax Income'].iloc[0]
            return tax_provision / pretax_income if pretax_income != 0 else 0.21
        
        # Default tax rate if calculation is not possible
        return 0.21
    
    def calculate_cost_of_equity(self):
        """
        Calculates the cost of equity using the CAPM formula.

        Returns:
            float: The cost of equity
        """
        return self.risk_free_rate + self.beta * (self.market_return - self.risk_free_rate)

    def calculate_cost_of_debt(self):
        """
        Calculates the cost of debt based on the company's interest expense and debt value.

        Returns:
            float: The cost of debt
        """
        income_statement = self.stock.financials.T

        if 'Interest Expense' in income_statement.columns and self.debt_value != 0:
            interest_expense = income_statement['Interest Expense'].iloc[0]
            return interest_expense / self.debt_value
        
        # Default cost of debt if data is missing
        return self.risk_free_rate + self.market_bond_spread

    def calculate_wacc(self):
        """
        Calculates the WACC by weighting the cost of equity and debt by their respective proportions of the company's total value.

        Returns:
            float: The WACC
        """
        # Calculate the proportion of equity and debt
        total_value = self.equity_value + self.debt_value
        equity_proportion = self.equity_value / total_value if total_value != 0 else 0
        debt_proportion = self.debt_value / total_value if total_value != 0 else 0

        wacc = (
            equity_proportion * self.calculate_cost_of_equity() +
            debt_proportion * self.calculate_cost_of_debt() * (1 - self.tax_rate)
        )
        print(f"WACC: {wacc:.2%}")
        return wacc