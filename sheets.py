import pandas as pd
import json
import os
from google.oauth2 import service_account
import pygsheets

def sheetpost(df):
    # Pass credentials to get client
    
    info = json.loads(os.environ['SERVICE_ACCOUNT'])
    credentials = service_account.Credentials.from_service_account_info(info)
    client = pygsheets.authorize(service_account_file='service_account.json')

    # Access BD Document
    secrets = json.loads(os.environ['SECRETS'])
    sheet = client.open_by_key(secrets['bd_sheet'])

    alldata = sheet.worksheet_by_title('alldata')
    # df = pd.read_csv('test1.csv')
    # df.to_csv('test1.csv')
    # df.to_csv('test1.xls')

    alldata.set_dataframe(df, start=(1,1), copy_index=False)