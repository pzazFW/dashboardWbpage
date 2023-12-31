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
    fig = px.area(pivot_table, x='Month', y='Total')
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

def bar_chart(df):

    # Extract the project columns dynamically between 'Month' and 'Total'
    project_columns = df.columns[df.columns.get_loc('Month')+1:df.columns.get_loc('Total')]

    # Create a DataFrame with project parts and their total hours
    project_total_hours = df[project_columns].sum() 

    # Create a Plotly bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=project_total_hours.index, y=project_total_hours.values))

    # Add labels to the x-axis and y-axis
    fig.update_xaxes(title_text='Projects')
    fig.update_yaxes(title_text='Hours')

    # Convert the Plotly figure to HTML div
    bar_chart_div = fig.to_html(full_html=False)

    return bar_chart_div

def table_div(df):

    # Sort the DataFrame by the 'Date' column in descending order
    df = df.sort_values(by='Date', ascending=False)
    
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Code','Date','Description'],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.Code, df.Date.dt.strftime("%Y-%m-%d"), df.Description],
                fill_color='lavender',
                align='left'))
    ])
    table_div = fig.to_html(full_html=False)

    return table_div