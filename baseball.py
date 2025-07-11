import pandas as pd
import gspread

from prizepicksscrape import call_endpoint
from scoresandoddsscrape_baseball import get_odds_data

gc = gspread.service_account(filename='peak-apparatus-465118-e6-a206e52e32e9.json')

# Open the spreadsheet
sh = gc.open("OverUnderOdds")

# Select a sheet
worksheet = sh.worksheet("Baseball")

odds_url = 'https://www.scoresandodds.com/mlb/props/'
prizepicks_url = 'https://partner-api.prizepicks.com/projections?league_id=2'

# Get Odds from ScoresAndOdds
odds_df = get_odds_data(odds_url)

#Get Lines from Prizepicks
picks_df = call_endpoint(prizepicks_url, include_new_player_attributes=True)

# Adds over value to all scores
picks_df['attributes.line_score'] = 'o' + picks_df['attributes.line_score'].astype(str)

# Adds under lines where applicable
picks_df['attributes.adjusted_odds'] = picks_df['attributes.adjusted_odds'].notna()
grouped_by_boolean = picks_df.loc[picks_df['attributes.adjusted_odds'] == False]
grouped_by_boolean['attributes.line_score'] = grouped_by_boolean['attributes.line_score'].str.replace('o', 'u')
picks_df = pd.concat([picks_df, grouped_by_boolean], ignore_index=True)

# Merges odds with prizepicks list
merged_df = pd.merge(picks_df, odds_df, on=["attributes.line_score", "attributes.name", "attributes.stat_type"], how='left')

available_df = merged_df.loc[picks_df['attributes.is_live'] == False]

# Create a new DataFrame with only the desired columns
columns_to_keep = ['attributes.line_score','attributes.odds_type','attributes.start_time','attributes.stat_type','attributes.name','Odds']
final_df = available_df[columns_to_keep]

final_df = final_df.fillna('')

final_df['Odds'] = final_df['Odds'].replace('', '0').astype(float)

# Sort values most to least likely
final_df = final_df.sort_values(by='Odds')

# Write data to the sheet
worksheet.update([final_df.columns.values.tolist()] + final_df.values.tolist())