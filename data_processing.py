import pandas as pd
from datetime import datetime
from flask import request

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

    # Pivot table to get total hours by month and category for the current year
    pivot_table = df.pivot_table(values='Hours', index=['Month'], columns='Code', aggfunc='sum', fill_value=0)

    # Summing up all codes for each month to get a 'Total' column
    pivot_table['Total'] = pivot_table.sum(axis=1)

    return pivot_table


def filter_timeframe(df, start_date, end_date):

    try:
        # Convert the dates to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        # Use the oldest date from your data if start_date is not provided
        if not start_date:
            start_date = oldest_date = df['Date'].min().strftime('%Y-%m-%d')
    try:
        # Convert the dates to datetime objects
        end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        # Use today's date if end_date is not provided
        if not end_date:
            end_date = datetime.today().strftime('%Y-%m-%d')


    # Assuming 'df' is your main DataFrame and it's globally accessible
    # Filter the dataframe
    try:
        filtered_df = df[(df['Date'].dt.to_timestamp() >= start_date) & (df['Date'].dt.to_timestamp() <= end_date)]
    except:
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]


    return filtered_df, start_date, end_date
