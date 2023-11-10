from get_access_token import get_access_token
from get_file_data import get_file_data
from data_processing import clean

# This is the modified function that includes your actual credentials and file path
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

    # Output the data
    print(df)  # Just show the first few rows

if __name__ == "__main__":
    main()
    app_


# Don't forget to define the `get_access_token` and `get_file_data` functions as


"""
try:
        # Get the access token
        access_token = get_access_token(client_id, client_secret, tenant_id)
        print("Successfully obtained access token.")

        # Retrieve the file data
        df = get_file_data(access_token, file_path)
        print("Successfully retrieved file data.")

        # Output the data
        print(df.head())  # Just show the first few rows

    except Exception as e:
        print("An error occurred:", e)"""