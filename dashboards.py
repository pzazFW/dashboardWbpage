import pandas as pd
from datetime import datetime
import plotly.express as px
import matplotlib.pyplot as plt
from pandas.plotting import table
import plotly.io as pio

def interactive_area_chart(pivot_table):
    
    pio.renderers.default = 'notebook'

    # Resetting index to use 'Month' as a column
    pivot_table.reset_index(inplace=True)

    # Change Month to string
    pivot_table['Month'] = pivot_table['Month'].dt.to_timestamp().strftime('%B %Y')

    # Get the current year
    current_year = datetime.now().year

    # Creating an interactive area plot with Plotly
    fig = px.area(pivot_table, x='Month', y='Total', title=f'{current_year} - Total Hours/Month')
    fig.show()