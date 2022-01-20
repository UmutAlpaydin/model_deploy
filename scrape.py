import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import asyncio
import json

import aiohttp

from understat import Understat



# url = 'https://understat.com/league/EPL'

# #Create a handle, page, to handle the contents of the website
# page = requests.get(url)
# #Store the contents of the website under doc
# soup = BeautifulSoup(page.text, 'html.parser')
# print(soup.findAll("div", {'id': 'league-chemp'}))
# table_div = soup.find('div' , {'id': 'league-chemp'})
# table = table_div.find('table')
# content = str(table)

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re
# Entering the league's  link
link = "https://understat.com/league/EPL"
res = requests.get(link)
soup = BeautifulSoup(res.content,'lxml')
scripts = soup.find_all('script')
# Get the table 
strings = scripts[2].string 
# Getting rid of unnecessary characters from json data
ind_start = strings.index("('")+2 
ind_end = strings.index("')") 
json_data = strings[ind_start:ind_end] 
json_data = json_data.encode('utf8').decode('unicode_escape')
data = json.loads(json_data)


df = pd.DataFrame(data.values())
df = df.explode("history")
h = df.pop("history")
df = pd.concat([df.reset_index(drop=True), pd.DataFrame(h.tolist())], axis=1)
df = df.infer_objects()


table = df.groupby(['title']).agg({'wins': 'sum', 'draws': 'sum', 'loses': 'sum', 'scored': 'sum', 'missed': 'sum', 'pts': 'sum', 'xG': 'sum', 'xGA': 'sum', 'xpts': 'sum', 'npxG': 'sum', 'npxGA': 'sum', 'deep': 'sum', 'deep_allowed': 'sum'}).reset_index()
table = table.sort_values(by=['pts'], ascending=False)

# You could uncomment next lines to add a ranking format 

# Position = [i for i in range(1,21)]
# table['Pos'] = Position
# table.set_index('Pos', inplace=True)

csv_table = table[['xG', 'xGA', 'pts', 'xpts']]
csv_table.to_csv('football.csv', index=None)

# x_train = table[['xG', 'xGA', 'pts']].values
# y_train = table['xpts'].values
