from get_access_token import get_access_token
from get_file_data import get_file_data
from data_processing import clean, filter_timeframe, df_pivot_table
from flask import Flask, render_template, request, redirect, url_for
from dashboards import interactive_area_chart, bar_chart
from dashboards import table_div
from datetime import datetime, timedelta
from plotly.offline import plot


app = Flask(__name__)

# This is the modified function that includes your actual credentials and file path
@app.route('/', methods=['GET', 'POST'])
def main():
    
    # Place your credentials here
    tenant_id = '0d5373f9-30b8-47f7-a96b-e9fff2b2fb97'
    client_id = 'b4ff2a28-c009-4136-a643-74dd1f50e20c'
    client_secret = 'tmD8Q~JwrZSas4_Q4AAfpATc8po5sbavpeilzbmi'
    item_id = '01UZTENSJO27HBKLOEZBAYPQ3TTSCQLNZO'
    site_id = 'pazsolutions-my.sharepoint.com,bbd1d293-c56f-4f3a-80bd-d3401eee5f27,52d4199d-f4c0-45ac-bd1e-f5bc33e128df'
    sheet_name = 'TotalTimeReport'
    
    now = datetime.now()
    start_date = None
    end_date = None

    # Get the access token
    access_token = get_access_token(client_id, client_secret, tenant_id)
    print("Successfully obtained access token.")
    
    # Retrieve the file data
    df = get_file_data(sheet_name, access_token, site_id, item_id)
    print("Successfully retrieved file data.")

    # Preprocess and clean data
    df = clean(df)
    df_original = df

    # Get project codes 
    project_codes = df['Code'].unique().tolist()

    # Initialize selected_code with all project codes by default
    selected_code = project_codes.copy()
    
    if request.method == 'POST':
        
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # Filtered timeframe
        df, start_date, end_date = filter_timeframe(df, start_date, end_date)

        if 'clear' in request.form:
            # Reset filters and load the default data view
            df = df_original # load your default DataFrame
            selected_code = df_original['Code'].unique().tolist()
            start_date = None
            end_date = None

        # Handle "This Month" button
        elif 'this_month' in request.form:
            start_date = now.replace(day=1)
            # To get the end date of the current month, we add one month to the start date (day=1 of the next month) 
            # and then subtract one day to get the last day of the current month
            end_date = (now.replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            df = df_original[(df_original['Date'] >= start_date) & (df_original['Date'] <= end_date)]
        
        # Handle "This Year" button
        elif 'this_year' in request.form:
            start_date = datetime(now.year, 1, 1)   
            end_date = datetime(now.year, 12, 31)
            df = df_original[(df_original['Date'] >= start_date) & (df_original['Date'] <= end_date)]
        
        # Handle project code selection
        selected_post_codes = request.form.getlist('project_code')
        if selected_post_codes:
            selected_code = selected_post_codes
            df = df[df['Code'].isin(selected_code)]
        else:
            # Get project codes 
            project_codes = df['Code'].unique().tolist()

            # Initialize selected_code with all project codes by default
            selected_code = project_codes.copy()
    else:
        print("No filter used")
        start_date = None
        end_date = None

    # Make pivot table
    pivot_table = df_pivot_table(df)

    # Create area charts
    area_chart_div = interactive_area_chart(pivot_table)

    # Get total hours
    total_hours = df['Hours'].sum()

    # Create a bar chart
    bar_chart_div = bar_chart(pivot_table)

    # Create table
    table_divs = table_div(df)

    try:
        # Format dates as strings in "YYYY-MM-DD" format if they are not None
        start_date = start_date.strftime('%Y-%m-%d') if start_date else None
        end_date = end_date.strftime('%Y-%m-%d') if end_date else None
    except:
        print("Already formatted")

    return render_template('index.html', total_hours = total_hours, plot_div=area_chart_div, bar_chart_div=bar_chart_div,  table_div=table_divs, project_codes=project_codes, selected_code=selected_code, start_date = start_date, end_date = end_date)    

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')