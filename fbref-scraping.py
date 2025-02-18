import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time

comm = re.compile("<!--|-->")
link_fb = 'https://fbref.com/en/comps/17/2012-2013/stats/2012-2013-Segunda-Division-Stats'

# FBREF
match_page_fb = requests.get(link_fb)   #Entra a la pagina de la liga nacional
match_soup_fb = BeautifulSoup(comm.sub('', match_page_fb.text), 'lxml')
header = match_soup_fb.find('table', {'id': 'stats_standard'}).find('thead').find_all('tr')[1]
table = match_soup_fb.find('table', {'id': 'stats_standard'}).find('tbody').find_all('tr')
header_list = [x.text for x in header if x.text not in ['\n', 'Born', 'Starts', '90s', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR']][1:-4] # Saca Header con stats relevantes para usarlo de header en Pandas
print(header_list)
data = []
player_links_fb = []
for i in table:
    if i.find('td', {'data-stat': 'player'}) and i.find('td', {'data-stat': 'age'}).text and int(i.find('td', {'data-stat': 'age'}).text) < 24:
        player_links_fb.append(i.find('td', {'data-stat': 'player'}).find('a', href=True)['href'])
    
    row_data = []
    for x in i.find_all('td'):
        if x.get('data-stat') in ['player', 'nationality', 'position', 'team', 'age', 'games', 'minutes', 'goals', 'assists', 'goals_assists'] and i.find('td', {'data-stat': 'age'}).text and int(i.find('td', {'data-stat': 'age'}).text) < 24:
            if x.get('data-stat') != 'team':
                row_data.append(x.text) #Saca las casillas dependiendo de si la información es la relevante
            else:
                row_data.append(re.sub('-', ' ', re.sub('-Stats', '', x.find('a')['href'].split('/')[-1])).lower())
    data.append(row_data)
    
df = pd.DataFrame(data, columns=header_list)
for x in header_list[4:]: # Convierte los valores numéricos de str a numeric
    df[x] = df[x].str.replace(',', '')
    df[x] = pd.to_numeric(df[x], errors='coerce')

df = df[df['Age'] < 24] # Filtra los jugadores para dejar solo los menores de 24
df['player_link'] = player_links_fb

def sub_and(text):
    return re.sub(' and ', ' & ', text)

df = df.rename(columns={'Player': 'player', 'Squad': 'team', 'Age': 'age'})
df['player'] = df['player'].str.lower()
df['team'] = df['team'].apply(sub_and)

print(player_links_fb)