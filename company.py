import yfinance as yf
import pandas as pd
from keys import FinKeys, FinStatement

class Company:
    def __init__(self, ticker):
        self.ticker = ticker
        self.info = {}
        self.financial_data = {}
        self.shares_outstanding = None
        self.cash = None
        self.debt = None

        self.download_company_data()
        
    def download_company_data(self):
        stock = yf.Ticker(self.ticker)
        
        # Download company information
        self.info = stock.info
        self.name = self.info.get('longName', None)
        self.market_cap = self.info.get('marketCap', None)
        self.industry = self.info.get('industry', None)
        self.sector = self.info.get('sector', None)
        self.enterprise_value = self.info.get('enterpriseValue', None)
        
        # Download financial data
        self.financial_data = {
            FinStatement.CASHFLOW.value: self.reverse_dataframe(stock.cashflow),
            FinStatement.BALANCE_SHEET.value: self.reverse_dataframe(stock.balance_sheet),
            FinStatement.INCOME.value: self.reverse_dataframe(stock.income_stmt)
        }
        
        self.shares_outstanding = self.info.get(FinKeys.SHARES_OUTSTANDING.value, None)
        self.cash = self.get_latest_value(FinStatement.BALANCE_SHEET.value, FinKeys.CASH.value)
        self.debt = self.get_latest_value(FinStatement.BALANCE_SHEET.value, FinKeys.DEBT.value)
        
    def reverse_dataframe(self, df):
        return df.iloc[::-1]
    
    def get_latest_value(self, statement, key):
        try:
            return self.financial_data[statement].loc[key].dropna().iloc[-1]
        except KeyError:
            return None
    
    def get_data_range(self, statement, key):
        df = self.financial_data[statement]
        try:
            data_series = df.loc[key].dropna()
            return data_series
        except KeyError:
            print(f"[ERROR] Key '{key}' not found in statement '{statement}' for ticker '{self.ticker}'.")
            return pd.Series()
    
    def print_metrics(self):
        for statement, df in self.financial_data.items():
            print(f"\nMetrics from {statement}:")
            print(df.index.tolist())
