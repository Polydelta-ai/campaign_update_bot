import requests
import json
import pandas as pd

from buildmsg import BuildMsg

def slackpost(campaign, df):

	# Load Credentials
	with open('secrets.json') as source:
		secrets = json.load(source)
	slack_url = secrets[campaign]

	data = {
		"blocks": [
			{
				"type": "header",
				"text": {
					"type": "plain_text",
					"text": "{} Sector BD Campaign Update".format(campaign.capitalize()),
				}
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": BuildMsg(campaign, df)
				}
			}
		]
	}


	response = requests.post(slack_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

	print('Response: ' + str(response.text))
	print('Response code: ' + str(response.status_code))

if __name__ == "__main__":
	df = pd.read_csv('test1.csv')
	for i in ('public', 'private'):
		slackpost(i, df)