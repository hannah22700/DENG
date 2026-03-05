import requests
import json
import pandas as pd
from io import StringIO

def get_stock_data():
    url = "https://api.openparldata.ch/v1/persons?output_format=csv&fields=id,name "
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.text
        return data
    else:
        return None

data = get_stock_data()

print(data)

df = pd.read_csv(StringIO(data))

print(df)