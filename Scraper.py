import html5lib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import sys

website = urlopen("https://www.basketball-reference.com/draft/NBA_2020.html")
soup = BeautifulSoup(website, "html5lib")
column_titles = [table_headers.getText() for table_headers in soup.findAll('tr', limit = 2)[1].findAll('th')]

#construct a data frame
df = pd.DataFrame()
for yr in range(2000, 2020): #scraping data from individual drafts
    url_current = f"https://www.basketball-reference.com/draft/NBA_{yr}.html"
    
    website = urlopen(url_current)
    soup = BeautifulSoup(website, 'html5lib') #creating the beautfulsoup object to scrape html data

    #consolidating individual player data
    rows = soup.findAll('tr')[2:]

    #getting all of the text for each row of player data
    player_data = [[table_data.getText() for table_data in rows[i].findAll(['td', 'th'])] for i in range(len(rows))]

    #Create data frame for annual draft data
    year = pd.DataFrame(player_data, columns = column_titles)

    #insert columns for each individual draft year
    year.insert(0, "Draft_Year", yr)

    #append each year to the overall datafram
    df = df.append(year, ignore_index = True)

#append "Per_game" to stats pertaining to per game values
df.columns.values[15:19] = [df.columns.values[15:19][col] + "_pg" for col in range(4)]

#delete obsolete Rk column
df.drop('Rk', axis = 'columns', inplace = True)

#convert all possible numeric data points to numbers
df['Draft_Year'] = pd.to_numeric(df['Draft_Year'], errors='coerce')
df['Pk'] = pd.to_numeric(df['Pk'], errors='coerce')
df['Yrs'] = pd.to_numeric(df['Yrs'], errors='coerce')
df['G'] = pd.to_numeric(df['G'], errors='coerce')
df['MP'] = pd.to_numeric(df['MP'], errors='coerce')
df['PTS'] = pd.to_numeric(df['PTS'], errors='coerce')
df['TRB'] = pd.to_numeric(df['TRB'], errors='coerce')
df['AST'] = pd.to_numeric(df['AST'], errors='coerce')
df['FG%'] = pd.to_numeric(df['FG%'], errors='coerce')
df['3P%'] = pd.to_numeric(df['3P%'], errors='coerce')
df['FT%'] = pd.to_numeric(df['FT%'], errors='coerce')
df['MP_pg'] = pd.to_numeric(df['MP_pg'], errors='coerce')
df['PTS_pg'] = pd.to_numeric(df['PTS_pg'], errors='coerce')
df['TRB_pg'] = pd.to_numeric(df['TRB_pg'], errors='coerce')
df['AST_pg'] = pd.to_numeric(df['AST_pg'], errors='coerce')
df['WS'] = pd.to_numeric(df['WS'], errors='coerce')
df['WS/48'] = pd.to_numeric(df['WS/48'], errors='coerce')
df['BPM'] = pd.to_numeric(df['BPM'], errors='coerce')
df['VORP'] = pd.to_numeric(df['VORP'], errors='coerce')

#remove full null rows if the player field is empty
df = df[df.Player.notnull()]

#replace all NaNs (not numbers) with 0
df = df.fillna(0)

#rename win shares column for readability
df.rename(columns = {'WS/48':'Win_Shares_per_48'}, inplace = True)

#Change appropriate fields to integers
df.loc[:, 'Yrs':'AST'] = df.loc[:, 'Yrs':'AST'].astype(int)

#draft pick value changed to int
df['Pk'] = df['Pk'].astype(int)

df.to_csv("draft_data_2000s.csv")