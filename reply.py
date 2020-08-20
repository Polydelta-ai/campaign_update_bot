import requests
import json
import pandas as pd
import re
import os
from sheets import sheetpost
from slackpost import slackpost


def buildDataFrame(response_object):
  df = pd.DataFrame(response_object)
  
  # Format Data Frame
  df.sort_values(by=['created'], ascending=False, inplace=True, ignore_index=True)

  # Create reply rate column
  df['replyRate'] = df['repliesCount']/df['deliveriesCount']

  # Replace NaNs with 0
  df['replyRate'] = df['replyRate'].fillna(0)

  # Reformat reply Rate as percentage
  df['replyRate'] = pd.Series(["{0:.2f}%".format(val * 100) for val in df['replyRate']])

  # strip out JFP campaigns
  df = df[df['ownerEmail'] != 'jay@jf-p.com']

  # reformat labels
  def updatelabels(label):
    label = re.sub("([a-z])([A-Z])","\g<1> \g<2>",label)
    words = label.split(' ')
    words = [word.capitalize() for word in words]
    label = " ".join(words)
    
    return label

  df.columns = [updatelabels(label) for label in df.columns]

  return df

def getReplyStats():
  # Get API Credentials
  
  secrets = json.loads(os.environ['SECRETS'])
  print(secrets)

  # Base API request URL
  url = "https://api.reply.io/v1/campaigns"

  # Payload and Headers for request
  payload = {}
  headers = {
    'x-api-key': secrets['reply']
  }

  # Make request and parse response
  response = requests.request("GET", url, headers=headers, data = payload)
  responseJSON = json.loads(response.text)  # this returns a list

  return responseJSON

def reply(event=None, context=None):
    # get data from reply.io and build a DataFrame
    r = getReplyStats()
    df = buildDataFrame(r)
    
    # post dataframe to Google Sheets
    sheetpost(df)
    
    # post dataframe in slack
    for i in ('public', 'private'):
      slackpost(i, df)