import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_odds_data(base_url):

    data = []

    nba_props_list = {'points':'Points', 'rebounds':'Rebounds', 'assists':'Assists', 'blocks':'Blocks', 'steals':'Steals', '3-pointers':'3-Pointers Made', 'points-&-rebounds':'Points + Rebounds', 'points-&-assists':'Points + Assists', 'points,-rebounds,-&-assists':'Points + Rebounds + Assists', 'rebounds-&-assists':'Assists + Rebounds'}

    for propKey, propValue in nba_props_list.items():
        page = requests.get(base_url+propKey)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find('ul', class_ = 'table-list')

        rows = results.find_all('li', class_ = 'border')

        for row in rows:
            name_div = row.find('div', class_='props-name')
            name = name_div.find('span')
            if name is not None:
                odds_list = row.find_all('div', class_='game-odds best')
                for odds in odds_list:
                    utils = [name.text]
                    line = odds.find('span', class_='data-moneyline')
                    if line is None:
                        utils.append('NA')
                        utils.append('NA')
                    else:
                        utils.append(line.text)
                        utils.append(line.text[0])
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

    df = pd.DataFrame(data,columns=["Name","Line","O/U","Odds","Type"])

    return df

#print(oddsDf.sort_values(by='Odds'))

