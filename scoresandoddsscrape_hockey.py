import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_nhl_data():
    base_url = 'https://www.scoresandodds.com/nhl/props/'

    data = []

    mlb_props_list = {'goals':'Goals', 'shots-on-goal':'Shots On Goal', 'assists':'Assists', 'points':'Points', 'blocked-shots':'Blocked Shots'}

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
                    elif 'o' not in line.text and 'u' not in line.text:
                        utils.append('o0.5')
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

    df = pd.DataFrame(data,columns=["attributes.name","scores_line_score","Odds","attributes.stat_type"])

    return df