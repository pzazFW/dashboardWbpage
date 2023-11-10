import pandas as pd

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

    print(df.dtypes)
    return df