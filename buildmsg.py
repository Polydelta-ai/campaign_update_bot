import pandas as pd

def BuildMsg(campaign, df):

    # Filter for Reply.io DataFrame for campaign type (public or private)
    campaign_df = df['Name'].str.contains(campaign.capitalize()) | df['Name'].str.contains(campaign.lower()) #mask
    campaign_df = df[campaign_df] #mask applied
    campaign_data = campaign_df.to_dict(orient='list') #create list
    
    # Message strings
    sector = "<!here>Here's the latest update on the {sector} sector BD campaigns." 
    campaigns_q = "\n*There are {number_of_campaigns} active campaigns*" 
    detail = "    • {campaign_name} : {number_of_deliveries} deliveries - Current Response Rate {current_response_rate}" 
    link = "\n*See the full report <https://docs.google.com/spreadsheets/d/1MZaYX6VNYFoqbWQ3Dy6WmZLWQjhaZHoCq5QXwnZ0uUU/edit?usp=sharing|here>*"  
    
    # Parameters
    params = {
        'sector' : campaign,
        'number_of_campaigns' : str(len(campaign_df)),
    }
    details = []
    for i in range(len(campaign_df)):
        detail_params = {
            'campaign_name' : campaign_data['Name'][i],
            'number_of_deliveries' : campaign_data['Deliveries Count'][i],
            'current_response_rate' : campaign_data['Reply Rate'][i],
        }
        details.append(detail.format(**detail_params))

    # Build Message
    sector = sector.format(**params)
    campaigns_q = campaigns_q.format(**params)
    details = '\n'.join(details)
    msg = '\n'.join([sector, campaigns_q, details, link])

    return msg