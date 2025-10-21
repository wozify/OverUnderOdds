import pandas as pd
pd.set_option('mode.chained_assignment', None)

from combiner import create_spreadsheet

#football = create_spreadsheet('Football')
#baseball = create_spreadsheet('Baseball')
#wnba = create_spreadsheet('WNBA')
#hockey = create_spreadsheet('Hockey')
basketball = create_spreadsheet('Basketball')

#football.to_csv('football.csv', index=False)
#baseball.to_csv('baseball.csv', index=False)
#wnba.to_csv('wnba.csv', index=False)
#hockey.to_csv('hockey.csv', index=False)
basketball.to_csv('basketball.csv', index=False)