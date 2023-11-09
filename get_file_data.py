import pandas as pd
from io import BytesIO
import requests

def get_file_data(access_token, site_id, item_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    #encoded_file_path = requests.utils.quote(file_path)  # URL encode the file path
    #download_url = f"https://graph.microsoft.com/v1.0/me/drive/root:{encoded_file_path}:/content"
    # For SharePoint use: 
    download_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{item_id}//workbook/worksheets/TotalTimeReport/usedRange"

    response = requests.get(download_url, headers=headers)
    response.raise_for_status()

    # Now you parse the JSON to get the actual values
    json_response = response.json()
    values = json_response.get('text', [])  # Assuming 'text' contains the cell values

    # Create the DataFrame
    df = pd.DataFrame(values)
    #pd.set_option('display.max_rows', None)
    #df = pd.read_excel(BytesIO(response.content))
    return df