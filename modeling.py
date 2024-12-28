import numpy as np
from keys import FinStatement, FinKeys

class ProjectAssumptions:
    def __init__(self, financial_data=None):
        """
        Initializes the ProjectAssumptions class with financial data.

        :param financial_data: A dictionary containing financial data, 
                               where keys are FinancialStatement enum values.
        """
        self.financial_data = financial_data or {}
    
    def calculate_growth_rate(self, statement: FinStatement, key: FinKeys, low_threshold: float = 25, high_threshold: float = 75):
        """
        Calculates the average growth rate for a given financial key within the specified thresholds.

        :param statement: A FinancialStatement enum value representing the type of financial statement.
        :param key: A FinancialKeys enum value representing the specific financial metric.
        :param low_threshold: The lower percentile threshold for filtering growth rates.
        :param high_threshold: The upper percentile threshold for filtering growth rates.
        :return: The average filtered growth rate.
        :raises: KeyError if the financial key is not found in the data.
                 ValueError if no growth rates fall within the specified thresholds.
        """
        try:
            # Ensure the data is in numerical format
            data = self.financial_data[statement.value].loc[key.value].astype(float).sort_index(ascending=True)
            yoy_growth = data.pct_change().dropna()

            lower, upper = np.percentile(yoy_growth, [low_threshold, high_threshold])
            filtered_growth = yoy_growth[(yoy_growth >= lower) & (yoy_growth <= upper)]
            
            if filtered_growth.empty:
                raise ValueError("No growth rates within the specified thresholds.")

            return filtered_growth.mean()
        
        except KeyError:
            raise KeyError(f"The key '{key.value}' does not exist in the '{statement.value}' data.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while calculating the growth rate: {e}")
