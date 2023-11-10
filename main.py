from get_access_token import get_access_token
from get_file_data import get_file_data
from data_processing import clean
from flask import Flask, render_template
from dashboards import interactive_area_chart
from data_processing import df_pivot_table
from datetime import datetime 
from dashboards import create_pivot_table_figure
from plotly.offline import plot

app = Flask(__name__)

# This is the modified function that includes your actual credentials and file path
@app.route('/')
def main():
    # Place your credentials here
    tenant_id = '0d5373f9-30b8-47f7-a96b-e9fff2b2fb97'
    client_id = 'b4ff2a28-c009-4136-a643-74dd1f50e20c'
    client_secret = 'tmD8Q~JwrZSas4_Q4AAfpATc8po5sbavpeilzbmi'
    item_id = '01UZTENSJO27HBKLOEZBAYPQ3TTSCQLNZO'
    site_id = 'pazsolutions-my.sharepoint.com,bbd1d293-c56f-4f3a-80bd-d3401eee5f27,52d4199d-f4c0-45ac-bd1e-f5bc33e128df'
    sheet_name = 'TotalTimeReport'

    # Path to the Excel file on OneDrive
    file_path = '/Excel/Kalkyl ZC AB.xlsx'
    
    # Get the access token
    access_token = get_access_token(client_id, client_secret, tenant_id)
    print("Successfully obtained access token.")
    
    # Retrieve the file data
    df = get_file_data(sheet_name, access_token, site_id, item_id)
    print("Successfully retrieved file data.")

    #Preprocess and clean data
    df = clean(df)
 
    # Get the current year
    current_year = datetime.now().year

    # Filter the DataFrame for the current year
    df_current_year = df[df['Month'].dt.to_timestamp().dt.year == current_year]

    # Make pivot table for current year
    pivot_table_current_year = df_pivot_table(df_current_year)

    # Make pivot table for all data
    pivot_table = df_pivot_table(df)

    # Create area chart
    area_chart_div = interactive_area_chart(pivot_table_current_year)

    # Create pivot table chart
    pivot_table_fig = create_pivot_table_figure(pivot_table)
    pivot_table_div = plot(pivot_table_fig, output_type='div', include_plotlyjs=False)


    return render_template('index.html', plot_div=area_chart_div, pivot_table_div=pivot_table_div)

    

if __name__ == "__main__":
    app.run(debug=True)