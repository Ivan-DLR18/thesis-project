import requests
import re
from bs4 import BeautifulSoup
import json
import time
import pandas as pd

comm = re.compile("<!--|-->")

link = 'https://www.transfermarkt.mx/championship/startseite/wettbewerb/GB2/saison_id/2012'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

response = requests.get(link, headers=headers)

if response.status_code == 200:
    pass
else:
    print(f'Request failed with status code: {response.status_code}')

tm_soup = BeautifulSoup(comm.sub('', response.text), 'lxml')


table = tm_soup.find('div', {'id': 'yw1'}).find('tbody')
links_teams = [(x.find('a')['href'], x.find('a').get('title').lower()) for x in table.find_all('td') if 'hauptlink' in x.get('class')]
print(links_teams)
table_header = ['player', 'id', 'age', 'team', 'initial_value', 'value_1', 'value_2', 'max_value']

table_info = []
for team_tm in links_teams:
    team_link = team_tm[0]
    team_name_tm = team_tm[1]
    link = 'https://www.transfermarkt.mx' + team_link
    print(link)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    response_team = requests.get(link, headers=headers)

    if response_team.status_code == 200:
        pass # Print the content of the response
    else:
        print(f'Request failed with status code: {response_team.status_code}')

    team_tm_soup = BeautifulSoup(comm.sub('', response_team.text), 'lxml')
    team_tm_table = team_tm_soup.find('div', {'id': 'yw1'}).find('tbody').find_all(recursive=False)
    for player in team_tm_table:
        player_data = []
        player_data_analysis = [] # For transfer value analysis for the conference draft
        row_player = player.find('td', {'class': 'hauptlink'})

        player_info = row_player.find('a')['href'].split('/')
        player_id = player_info[-1]
        player_name = re.sub('-', ' ', player_info[1])

        player_age = re.findall(r'\((\d+)\)', player.find('td').find_next_siblings('td')[1].text)
        # print(player_name, player_id, int(player_age[0]))
        
        if not player_age or int(player_age[0]) > 24:
            print('Jugador ' + player_name + ' omitido')
            continue  
        
        print(player_name + ' - ' + player_id)
        player_value_res = requests.get('https://www.transfermarkt.mx/ceapi/marketValueDevelopment/graph/' + player_id, headers=headers).text
        player_value_dev = json.loads(player_value_res)['list']

        player_value_cell = player.find('td', {'class': 'rechts hauptlink'}).text.split()

        if len(player_value_cell) > 2 and player_value_cell[1] == 'mil':
            player_actual_value = float(player_value_cell[0])*1000
        elif len(player_value_cell) > 2 and player_value_cell[1] == 'mill.':
            player_actual_value = float(player_value_cell[0])*1000000
        else:
            player_actual_value = None
        
        
        player_data.append(player_name) # Agrega nombre del jugador
        player_data.append(player_id)
        player_data.append(int(player_age[0])) # Agrega edad del jugador
        player_data.append(team_name_tm) # Agrega equipo del jugador
        player_data.append(player_actual_value) # Agrega el valor del jugador al final de la temporada 2012/2013

        max_value = [(x['y'], int(x['datum_mw'].split('/')[-1])) for x in player_value_dev if int(x['datum_mw'].split('/')[-1]) < 2024 and int(x['datum_mw'].split('/')[-1]) >= 2013] # Agrega el valor máximo que el jugador alcanzó durante su carrera después del 2012

        year_control = 2013
        next_values = []
        for values in max_value:
            if values[1] != year_control and len(next_values) < 2:
                next_values.append((values[1], values[0]))
                year_control = values[1]
            else:
                if len(next_values) > 0 and len(next_values) <= 2 and values[1] == next_values[-1][0] and values[0] > next_values[-1][1]:
                    next_values[-1] = (values[1], values[0])
                else:
                    continue

        ##### FOR CONFERENCE DRAFT #####
        player_data_analysis.append(player_name) # Agrega nombre del jugador
        player_data_analysis.append(player_id)
        player_data_analysis.append(int(player_age[0])) # Agrega edad del jugador
        player_data_analysis.append(team_name_tm) # Agrega equipo del jugador
        player_data_analysis.append(player_actual_value) # Agrega el valor del jugador al final de la temporada 2012/2013

        year_control = 2015
        for value, year in max_value:
            if year > year_control:
                player_data_analysis.append(value)
                year_control = year
            else:
                year_control = year
        print('player_data_analysis:')
        print(player_data_analysis)
        ###############################

        try:
            player_data.append(next_values[0][1])
        except IndexError:
            player_data.append(None)
        try:
            player_data.append(next_values[1][1])
        except IndexError:
            player_data.append(None)

        max_value = [x['y'] for x in player_value_dev if int(x['datum_mw'].split('/')[-1]) < 2024 and int(x['datum_mw'].split('/')[-1]) >= 2013] # Agrega el valor máximo que el jugador alcanzó durante su carrera después del 2012
        
        if len(max_value) > 0:
            player_data.append(max(max_value)) # Agrega el valor máximo que el jugador alcanzó durante su carrera después del 2012
        else:
            player_data.append(None)

        table_info.append(player_data)
        time.sleep(1)

        print(player_data)

market_value_df = pd.DataFrame(table_info, columns=table_header)
# change file name as needed
market_value_df.to_csv('FRA-market-value.csv', index=False)
market_value_df

