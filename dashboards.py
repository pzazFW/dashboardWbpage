import pandas as pd
from datetime import datetime
import plotly.express as px
import matplotlib.pyplot as plt
from pandas.plotting import table
import plotly.io as pio
from plotly.offline import plot
from flask import Flask, render_template
import plotly.graph_objects as go

def interactive_area_chart(pivot_table):
    
    pio.renderers.default = 'notebook'

    # Resetting index to use 'Month' as a column
    pivot_table.reset_index(inplace=True)

    # Change Month to string format (assuming 'Month' is now a regular column containing datetime objects)
    pivot_table['Month'] = pivot_table['Month'].apply(lambda x: x.strftime('%B %Y'))

    # Get the current year
    current_year = datetime.now().year

    # Creating an interactive area plot with Plotly
    fig = px.area(pivot_table, x='Month', y='Total', title=f'{current_year} - Total Hours/Month')
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    #fig.show()

    return plot_div
    


def create_pivot_table_figure(pivot_table):
    # Assuming pivot_table is a DataFrame with the desired pivot table data
    figure = go.Figure(data=[go.Table(
        header=dict(values=list(pivot_table.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[pivot_table[col] for col in pivot_table.columns],
                   fill_color='lavender',
                   align='left'))
    ])
    
    # Optionally set the table layout or size here
    # figure.update_layout(...)

    return figure
