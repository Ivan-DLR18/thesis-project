import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time

data_attributes = []
season_id = ['130026', '140044', '150052']
for page in range(0,301,60): # La paginación funciona agregando &offset=60 porque en cada página caben 60 hasta que llega a 300, por eso 301
    if page:
        offset = f'&offset={page}'
    else:
        offset = ''
    print(offset)
    comm = re.compile("<!--|-->")
    link_page = 'https://sofifa.com/players?type=all&lg%5B%5D=17&aeh=24&showCol%5B0%5D=ae&showCol%5B1%5D=oa&showCol%5B2%5D=pt&showCol%5B3%5D=pac&showCol%5B4%5D=sho&showCol%5B5%5D=pas&showCol%5B6%5D=dri&showCol%5B7%5D=def&showCol%5B8%5D=phy&r=130026&set=true' + offset
    # Este link es tan específico porque modifica la búsqueda para que sea el FIFA 13 al 26 de julio que fue cuando acabó la temporada, filtra por Championship, edad y muestra columnas 
    # de atributos 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physical'

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0',}

    response_page = requests.get(link_page, headers=headers)
    
    if response_page.status_code == 200:
        data_header = ['player', 'player_link', 'age', 'team', 'overall', 'potential', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physical']

        page_soup = BeautifulSoup(comm.sub('', response_page.text), 'lxml')
        page_table = page_soup.find('table', {'class': 'table table-hover persist-area'}).find('tbody').find_all('tr', recursive=False) # Encuentra la tabla específica de los jugadores
        for row in page_table:
            data_row = []
            if int(row.find('td', {'data-col': 'ae'}).text) <= 24: # Filtro de edad
                name= row.find('td', {'class': 'col-name'}).find('a').get('aria-label').lower()
                age = int(row.find('td', {'data-col': 'ae'}).text)
                team_player = row.find('td', {'class': 'col-name'}).find_next_sibling('td', {'class': 'col-name'}).find('a', href=True).text.lower()
                player_link = row.find('td', {'class': 'col-name'}).find('a').get('href')
                txt_list = player_link.split('/')
                txt_list[3] = '?r='
                player_link = '{}/{}/{}{}{}&set=true{}'.format(*txt_list)


                # print(team_player)
                data_row.append(name)
                data_row.append(player_link)
                data_row.append(age)
                data_row.append(team_player)
                
                data_row += [int(x.find('span').text) for x in row.find_all('td', recursive=False) if x.get('data-col') and x.find('span')] # El numero del stat se encuentra en un elemento span, elemento que solo las columnas
                # útiles poseen, por lo que solo hace falta revisar si el elemento td tiene span para sacar el texto de overall, potential, etc. se le suma a data_row porque ya se había agregado el nombre
                
                print(data_row)
                data_attributes.append(data_row)
        time.sleep(3) # Tiempo de espera para que no me bloqueen los hijos de la vrg
    else:
        print(f'Request failed with status code: {response_page.status_code}')
        break

attributes = pd.DataFrame(data_attributes, columns=data_header)
attributes.to_csv('FRA-attributes.csv', index=False) # Lo exporta a un csv aparte para mejor control
attributes
