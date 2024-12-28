from flask import Flask, render_template, request
from company import Company
from dcf_models.operations import CashFlowOperationsDCF
from plotter import Plotter 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form['ticker']
        forecast_years = int(request.form['forecast_years'])

        # Instantiate the Company object
        company = Company(ticker)

        # Pass the Company object to DCF
        #dcf_calculator = NopatDCF(company, forecast_years)
        dcf_calculator = CashFlowOperationsDCF(company, forecast_years)
        dcf_calculator.calculate_dcf()
        equity_value = dcf_calculator.calculate_equity_value()
        intrinsic_share_price = dcf_calculator.calculate_intrinsic_share_price()

        # Calculate additional values
        total_dcf_value = dcf_calculator.dcf_table['Discounted FCF ($)'].sum()
        
        # Create plotter instance
        plotter = Plotter(dcf_table=dcf_calculator.dcf_table, company=company)
        
        # Generate interactive plots
        dcf_plot = plotter.create_dcf_plot()
        core_metrics_plot = plotter.create_financial_metrics_plot()

        # Prepare DataFrame for display in billions
        dcf_table_display = dcf_calculator.dcf_table.copy()
        dcf_table_display['Forecasted FCF ($)'] = dcf_table_display['Forecasted FCF ($)'] / 1e9
        dcf_table_display['Discounted FCF ($)'] = dcf_table_display['Discounted FCF ($)'] / 1e9

        # Rename columns for display
        dcf_table_display = dcf_table_display.rename(columns={
            'Forecasted FCF ($)': 'Forecasted FCF ($B)',
            'Discounted FCF ($)': 'Discounted FCF ($B)'
        })
        dcf_table_display = dcf_table_display.round(2)

        return render_template(
            'result.html', 
            table=dcf_table_display.to_html(classes='table table-striped', index=False),
            ticker=ticker,
            company = company,
            dcf_plot=dcf_plot,
            core_metrics_plot = core_metrics_plot,
            total_dcf_value=total_dcf_value / 1e9, 
            equity_value=equity_value / 1e9,  
            intrinsic_share_price=intrinsic_share_price,
            shares_outstanding=dcf_calculator.company.shares_outstanding,
            cash=dcf_calculator.company.cash / 1e9,  
            debt=dcf_calculator.company.debt / 1e9   
        )

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
