import pandas as pd
pd.set_option('display.max_columns', 500)
import requests

def call_endpoint(url, max_level=6):
    '''
    takes:
        - url (str): the API endpoint to call
        - max_level (int): level of json normalizing to apply
        - include_player_attributes (bool): whether to include player object attributes in the returned dataframe
    returns:
        - df (pd.DataFrame): a dataframe of the call response content
    '''
    resp = requests.get(url).json()
    pickable = resp['pickableIdToPickableMap']
    data = []
    for key, value in pickable.items():
        normalizedPickable = pd.json_normalize(value['pickable'])
        normalizedMarket = pd.json_normalize(value['activeMarket'])
        normalizedEntities = pd.json_normalize(value['pickable'], record_path='pickableEntities')
        normalizedMarketSelection = pd.json_normalize(value['activeMarket'], record_path='pickableMarketSelections')
        for index, row in normalizedMarketSelection.iterrows():
            line = ''
            ou = ''
            if 1 == row['statLinePropositionId']:
                line = ('o'+normalizedMarket['targetValue'].to_string(index=False))
                ou = 'o'
            elif 2 == row['statLinePropositionId']:
                line = ('u' + normalizedMarket['targetValue'].to_string(index=False))
                ou = 'u'
            utils = [normalizedEntities['displayName'].to_string(index=False), line,
                     normalizedPickable['marketCategory.marketName'].to_string(index=False), ou]
            data.append(utils)
    df = pd.DataFrame(data,columns=["Name","DK_Line","Type", 'O/U'])
    return df