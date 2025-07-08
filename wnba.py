import pandas as pd
import gspread

from draftkingsscrape import call_endpoint
from scoresandoddsscrape_nba import get_odds_data

gc = gspread.service_account(filename='peak-apparatus-465118-e6-a206e52e32e9.json')

# Open the spreadsheet
sh = gc.open("OverUnderOdds")

# Select a sheet
worksheet = sh.worksheet("WNBA")

odds_url = 'https://www.scoresandodds.com/wnba/props/'
draftkings_url = 'https://pick6.draftkings.com/?sport=WNBA&_data=routes%2F_index'

# Get Odds from ScoresAndOdds
odds_df = get_odds_data(odds_url)

odds_df.to_csv('wnba_odds.csv', index=False)

#Get Lines from Draftkings
picks_df = call_endpoint(draftkings_url)

picks_df.to_csv('wnba_draftkings.csv', index=False)

# Merges odds with prizepicks list
merged_df = pd.merge(picks_df, odds_df, on=["Name", "Type", "O/U"], how='left')

final_df = merged_df.fillna('')

final_df['Odds'] = final_df['Odds'].replace('', '0').astype(float)

# Sort values most to least likely
final_df = final_df.sort_values(by='Odds')

# Write data to the sheet
worksheet.update([final_df.columns.values.tolist()] + final_df.values.tolist())