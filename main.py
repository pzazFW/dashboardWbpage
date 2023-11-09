# This is the modified function that includes your actual credentials and file path
def main():
    # Place your credentials here
    tenant_id = '0d5373f9-30b8-47f7-a96b-e9fff2b2fb97'
    client_id = 'b4ff2a28-c009-4136-a643-74dd1f50e20c'
    client_secret = 'e516aa05-0015-4854-add2-2b894bf4c4db'

    # Path to the Excel file on OneDrive
    file_path = '/Excel/Kalkyl ZC AB.xlsx'

    try:
        # Get the access token
        access_token = get_access_token(client_id, client_secret, tenant_id)
        print("Successfully obtained access token.")

        # Retrieve the file data
        dataframe = get_file_data(access_token, file_path)
        print("Successfully retrieved file data.")

        # Output the data
        print(dataframe.head())  # Just show the first few rows

    except Exception as e:
        print("An error occurred:", e)

# Don't forget to define the `get_access_token` and `get_file_data` functions as
