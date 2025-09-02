import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_odds_data(base_url):

    data = []

    nfl_props_list = {'passing-yards':'Pass Yards', 'rushing-yards':'Rush Yards', 'receiving-yards':'Receiving Yards', 'receptions':'Receptions', 'touchdowns':'Rush+Rec TDs', 'passing-tds':'Pass TDs',
                      'completions':'Pass Completions', 'interceptions':'INT', 'pass-attempts':'Pass Attempts', 'rush-attempts':'Rush Attempts'}

    for propKey, propValue in nfl_props_list.items():
        page = requests.get(base_url + propKey)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find('ul', class_='table-list')

        rows = results.find_all('li', class_='border')

        for row in rows:
            name_div = row.find('div', class_='props-name')
            name = name_div.find('a')
            if name is not None:
                odds_list = row.find_all('div', class_='game-odds best')
                for odds in odds_list:
                    is_just_moneyline = False
                    utils = [name.text]
                    line = odds.find('span', class_='data-moneyline')
                    if 'o' in line.text or 'u' in line.text:
                        utils.append(line.text)
                    elif '+' in line.text or '-' in line.text:
                        is_just_moneyline = True
                        utils.append('o0.5')
                        mod_odd = line.text.replace("+", "")
                        if mod_odd == 'even':
                            mod_odd = '100'
                        utils.append(int(mod_odd))
                    else:
                        utils.append('o0.5')
                    value = odds.find('small', class_='data-odds best')
                    if value is None and not is_just_moneyline:
                        utils.append(1000)
                    elif not is_just_moneyline:
                        mod_odd = value.text.replace("+", "")
                        if mod_odd == 'even':
                            mod_odd = '100'
                        utils.append(int(mod_odd))
                    utils.append(propValue)

                    data.append(utils)

    df = pd.DataFrame(data, columns=["attributes.name","scores_line_score","Odds","attributes.stat_type"])

    return df

#print(oddsDf.sort_values(by='Odds'))

