import plotly.graph_objs as go
import plotly.io as pio
from keys import FinKeys,FinStatement

class Plotter:
    def __init__(self, dcf_table=None, company=None):
        self.dcf_table = dcf_table
        self.company = company

    def create_dcf_plot(self):
        plot_data = self.dcf_table[self.dcf_table['Year'] != 'Terminal Value'].copy()
        trace1 = go.Scatter(
            x=plot_data['Year'],
            y=plot_data['Forecasted FCF ($)'] / 1e9, 
            mode='lines+markers',
            name='Forecasted FCF',
            line=dict(color='royalblue', width=2),
            marker=dict(color='royalblue', size=8),
            hovertemplate='%{y:.2f} Billion $<extra></extra>' 
        )
        trace2 = go.Scatter(
            x=plot_data['Year'],
            y=plot_data['Discounted FCF ($)'] / 1e9, 
            mode='lines+markers',
            name='Discounted FCF',
            line=dict(color='firebrick', width=2),
            marker=dict(color='firebrick', size=8),
            hovertemplate='%{y:.2f} Billion $<extra></extra>' 
        )

        layout = go.Layout(
            title=dict(
                text='Forecasted and Discounted Cash Flows (in Billions)',
                x=0.5,  # Center the title
                y=0.9,  # Adjust the vertical position of the title
                xanchor='center',
                yanchor='top',
                font=dict(size=16)
            ),
            xaxis=dict(
                title='Year',
                tickmode='linear',
                showline=False,  # Remove axis line
                showgrid=False,  # Remove grid lines
                zeroline=False,  # Remove the x-axis baseline
            ),
            yaxis=dict(
                title='Cash Flow (Billion $)',
                showline=False,  # Remove axis line
                showgrid=False,  # Remove grid lines
                zeroline=False,  # Remove the y-axis baseline
            ),
            plot_bgcolor='rgba(0,0,0,0)',  
            paper_bgcolor='rgba(0,0,0,0)', 
            font=dict(color='black', size=12),
            hovermode='closest',  # Show hover information closest to the mouse pointer
            legend=dict(
                x=0.5,
                y=1,  # Position legend below the title
                xanchor='center',
                yanchor='bottom',
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)',
                orientation='h', 
            ),
            margin=dict(l=40, r=40, t=100, b=40),  # Adjust margins for minimal look
        )

        # Update figure layout to remove zoom and pan
        fig = go.Figure(data=[trace1, trace2], layout=layout)
        fig.update_layout(
            dragmode=False,  
            hovermode='closest',  
        )
        fig.update_xaxes(fixedrange=True)  # Disable zoom on x-axis
        fig.update_yaxes(fixedrange=True)  # Disable zoom on y-axis
        fig.update_traces(marker=dict(size=8), selector=dict(mode='markers'))

        plot_html = pio.to_html(fig, full_html=False)
        return plot_html

    def create_financial_metrics_plot(self):
        if self.company is None:
            raise ValueError("Company data is not provided")

        # Extract financial data
        financial_data = {
            'Revenue': self.company.get_data_range(FinStatement.INCOME.value, FinKeys.REVENUE.value),
            'EBITDA': self.company.get_data_range(FinStatement.INCOME.value, FinKeys.OPERATING_INCOME.value),
            'Net Income': self.company.get_data_range(FinStatement.INCOME.value, FinKeys.NET_INCOME.value)
        }

        # Initialize figure
        fig = go.Figure()

        # Define colors and line properties
        line_colors = {'Revenue': 'blue', 'EBITDA': 'green', 'EBIT': 'orange', 'Net Income': 'red'}
        
        # Iterate and add traces only for non-empty data
        for name, data in financial_data.items():
            if not data.empty:
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data.values / 1e9,
                    mode='lines+markers',
                    name=name,
                    line=dict(color=line_colors[name]),
                    marker=dict(size=10), 
                    hovertemplate='%{y:.2f}B $<extra></extra>'  
                ))

        # Consolidate layout updates
        fig.update_layout(
            xaxis=dict(
                title='Date',
                showline=False,
                showgrid=False,
                zeroline=False,
                fixedrange=True  # Disable zoom for better performance
            ),
            yaxis=dict(
                title='Value (Billion $)',
                showline=False,
                showgrid=False,
                zeroline=False,
                fixedrange=True  # Disable zoom for better performance
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='black', size=12),
            hovermode='closest',
            legend=dict(
                x=0.5,
                y=1.15,  # Position the legend higher up
                xanchor='center',
                yanchor='bottom',  # Align the bottom of the legend to the specified y value
                orientation='h',
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)',
            ),
            margin=dict(l=40, r=40, t=80, b=40),  # Slightly reduce top margin
            dragmode=False  
        )

        # Generate the HTML for the plot
        plot_html = pio.to_html(fig, full_html=False)
        return plot_html
