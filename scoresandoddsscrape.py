import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_odds_data(base_url):

    data = []

    mlb_props_list = {'strikeouts':'Pitcher Strikeouts', 'earned-runs-allowed':'Earned Runs Allowed', 'hits-allowed':'Hits Allowed', 'walks-allowed':'Walks Allowed', 'outs':'Pitching Outs', 'home-runs':'Home Runs', 'singles':'Singles', 'hits':'Hits', 'total-bases':'Total Bases', 'runs-batted-in':'RBIs', 'steals':'Stolen Bases', 'hits,-runs-&-rbis':'Hits+Runs+RBIs'}

    for propKey, propValue in mlb_props_list.items():
        page = requests.get(base_url+propKey)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find('ul', class_ = 'table-list')

        rows = results.find_all('li', class_ = 'border')

        for row in rows:
            name_div = row.find('div', class_='props-name')
            name = name_div.find('a')
            if name is not None:
                odds_list = row.find_all('div', class_='game-odds best')
                for odds in odds_list:
                    utils = [name.text]
                    line = odds.find('span', class_='data-moneyline')
                    if line is None:
                        utils.append('NA')
                    else:
                        utils.append(line.text)
                    value = odds.find('small', class_='data-odds best')
                    if value is None:
                        utils.append(1000)
                    else:
                        modOdd = value.text.replace("+", "")
                        if modOdd == 'even':
                            modOdd = '100'
                        utils.append(int(modOdd))
                    utils.append(propValue)

                    data.append(utils)

    df = pd.DataFrame(data,columns=["attributes.name","attributes.line_score","Odds","attributes.stat_type"])

    return df

#print(oddsDf.sort_values(by='Odds'))

