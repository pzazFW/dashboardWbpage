import pandas as pd
from datetime import datetime

# Clean the data
def clean(df):
    #set column names equal to values in row index position 0
    df.columns = df.iloc[0]

    #remove first row from DataFrame
    df = df[1:]

    # Change data types
    df['Date'] = pd.to_datetime(df['Date'])
    try:
        df['Hours'] = df.Hours.astype(float)
    except:
        df['Hours'] = df.Hours.str.replace(',', '.').astype(float)

    dtype_dict = df.dtypes.replace({'object': 'string'}).to_dict()
    df = df.astype(dtype_dict)

    #Data preprocess add month column
    df['Month'] = df['Date'].dt.to_period('M')

    return df

def df_pivot_table(df):
    # Get the current year
    current_year = datetime.now().year

    # Filter the DataFrame for the current year
    df_current_year = df[df['Month'].dt.to_timestamp().dt.year == current_year]

    # Pivot table to get total hours by month and category for the current year
    pivot_table_current_year = df_current_year.pivot_table(values='Hours', index=['Month'], columns='Code', aggfunc='sum', fill_value=0)

    # Summing up all codes for each month to get a 'Total' column
    pivot_table_current_year['Total'] = pivot_table_current_year.sum(axis=1)

    return pivot_table_current_year

