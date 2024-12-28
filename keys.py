from enum import Enum

class FinKeys(Enum):
    REVENUE = 'Total Revenue'
    OPERATING_INCOME = 'Operating Income'
    TAX_PROVISION = 'Tax Provision'
    PRETAX_INCOME = 'Pretax Income'
    DEPRECIATION = 'Depreciation And Amortization'
    CAPEX = 'Capital Expenditure'
    DEBT = 'Total Debt'
    CASH = 'Cash Cash Equivalents And Short Term Investments'
    CHANGE_IN_WORKING_CAPITAL = 'Change In Working Capital'
    FREE_CASH_FLOW = 'Free Cash Flow'
    SHARES_OUTSTANDING = 'sharesOutstanding'
    EBITDA = 'EBITDA'
    EBIT = 'EBIT'
    NET_INCOME = 'Net Income'

    CASH_FLOW_OPERATIONS = 'Operating Cash Flow' 
    INTEREST_EXPENSE = 'Interest Expense' 
    TAXES_PAID = 'Income Tax Paid Supplemental Data'  
    
class FinStatement(Enum):
    BALANCE_SHEET = 'balance_sheet'
    CASHFLOW = 'cashflow'
    INCOME = 'income_statement'