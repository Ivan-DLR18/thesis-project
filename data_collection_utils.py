import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time
from unidecode import unidecode

def get_page_player(id ,season):
    link_page = f'https://sofifa.com/player/{id}?r={season}&set=true'
    # Este link es tan específico porque modifica la búsqueda para que sea el FIFA 13 al 26 de julio que fue cuando acabó la temporada, filtra por Championship, edad y muestra columnas 
    # de atributos 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physical'

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0',}

    response_page = requests.get(link_page, headers=headers, allow_redirects=False)
    time.sleep(1)
    return response_page

def get_player_ovrl_pot(id):
    link_page = f'https://sofifa.com/api/player/history?id={id}'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0',}

    response_player = requests.get(link_page, headers=headers, allow_redirects=False)
    # print(response_player.status_code)
    player_history = json.loads(response_player.text)['data']
    # print(player_history)

    player_relevant = [[x[2], x[1], x[5]] for x in player_history if x[5] in ['130026', '140001', '140044', '150001', '150052', '160001']]
    player_final = []
    # print(player_relevant)
    # El siguiente pedazo de código es para sacar el overall y el potencial de cada temporada del jugador sin repetir
    for i in seasons_ids:
        check = False
        szn_options = [seasons_ids[i]['id1'], seasons_ids[i]['id2']]
        # print(player_final)
        # print(szn_options)
        for x in player_relevant:
            if x[2] in szn_options:
                check = True
                player_final.append(x)
                break
            else:
                continue
        if check:
            continue
        else:
            player_final.append(['','',''])
    time.sleep(1)
    return player_final

def sub_team(text):
    text = re.sub(' fc', '', text)
    text = re.sub('fc ', '', text)
    text = re.sub('cf ','', text)
    text = re.sub(' cf','', text)
    text = re.sub('a ii', 'a b', text)
    text = re.sub('d ii', 'd castilla', text)
    text = re.sub('ud ', '', text)
    text = re.sub('cd ', '', text)
    text = re.sub(' cd', '', text)
    text = re.sub('ad ', '', text)
    text = re.sub('sd ', '', text)
    text = re.sub('ce ', '', text)
    text = re.sub(' de huelva', '', text)
    text = re.sub(' huelva', '', text)
    text = re.sub(' de', '', text)
    text = re.sub(' and ', ' & ', text)
    if text[-1] == ' ':
        text = text[:-1]
    return text

def sub_and(text):
    return re.sub(' and ', ' & ', text)

def second_lastname_erase(text):
    name = text.split()[:2]
    return name[0] + ' ' + name[1]

def normalize_names(text):
    # Remove accents and replace 'ñ' with 'n'
    text = re.sub('-', ' ', text)
    text = re.sub("'", '', text)
    cleaned_text = unidecode(text)

    return cleaned_text

def get_top_tier(player_link):
    print('Analizando carrera de: ' + player_link)
    player_link = 'https://fbref.com' + player_link
    comm = re.compile("<!--|-->")

    fb_page = requests.get(player_link)
    fb_soup = BeautifulSoup(comm.sub('', fb_page.text), 'lxml')
    # print(fb_soup)
    table = fb_soup.find('table', {'id': 'stats_standard_dom_lg'}).find('tbody')
    def find_th_with_text_and_attribute(tag): # Función que busca elemento 'th' que tenga 'year_id' y que este sea '2012-2013'
        # Usé 2012-2013 porque necesito los años siguientes, por eso busca los next_siblings()
        return tag.name == 'th' and tag.get('data-stat') == 'year_id' and tag.text == '2012-2013'
    
    player_table = table.find(find_th_with_text_and_attribute).find_parent('tr').find_next_siblings('tr')
    
    years_explored = ['2023-2024']
    year_row = []
    for x in player_table:
        if x.find('td', {'data-stat': 'games'}).text != '0' and x.find('th', {'data-stat': 'year_id'}).text not in years_explored:
            year_row.append(x)
            years_explored.append(x.find('th', {'data-stat': 'year_id'}).text)

    elite = 0
    for i in year_row:
        try:                                                            
            career = int(re.findall(r'\d+', i.find('td', {'data-stat': 'comp_level'}).get('csk'))[-1])   # Encuentra el número de nivel de liga en el que jugó ese año y la categoría [tier, comp-level]                                                             
            
            if career in [9, 12, 13, 20, 11]:
                elite += 1
            else:
                pass
        except TypeError:                                                                           # Y las agrega a la lista tier y comp-level segun corresponda
            continue
    time.sleep(3)
            
    print('Análisis de carrera completo')

    return elite > 0, elite # (Temporadas en primera, máximo nivel de competencia)

def get_next_2(player_link):
    print('Analizando carrera de: ' + player_link)
    player_link = 'https://fbref.com' + player_link
    comm = re.compile("<!--|-->")

    fb_page = requests.get(player_link)
    fb_soup = BeautifulSoup(comm.sub('', fb_page.text), 'lxml')
    # print(fb_soup)
    table = fb_soup.find('table', {'id': 'stats_standard_dom_lg'}).find('tbody')
    def find_th_with_text_and_attribute(tag): # Función que busca elemento 'th' que tenga 'year_id' y que este sea '2012-2013'
        # Usé 2012-2013 porque necesito los años siguientes, por eso busca los next_siblings()
        return tag.name == 'th' and tag.get('data-stat') == 'year_id' and tag.text == '2012-2013'
    
    player_table = table.find(find_th_with_text_and_attribute).find_parent('tr').find_next_siblings('tr')
    
    years_explored = ['2023-2024']
    year_row = []
    for x in player_table:
        year_row_temp = x.find('th', {'data-stat': 'year_id'}).text # Encuentra el año en cada fila para analizarlo en la siguiente línea
        if year_row_temp and year_row_temp not in years_explored: # Quité la condición de haber jugado por lo menos un minuto porque eso 
            # solo aplica para elite, aquí nos interesa saber incluso si no jugó
            year_row.append(x)
            years_explored.append(x.find('th', {'data-stat': 'year_id'}).text)

    mp_next = [] # Matches Played siguientes temporadas
    min_next = [] # Minutes siguientes temporadas
    gls_next = [] # Goles siguientes temporadas
    asst_next = [] # Asistencias siguientes temporadas
    gls_asst_next = [] # Goles y asistencias siguientes temporadas
    next_stat_counter = 2 # Contador de cuántas siguientes temporadas se quieren
    for i in year_row:
        if next_stat_counter > 0:
            try:
                mp_next.append(int(re.sub(',', '', i.find('td', {'data-stat': 'games'}).text)))
            except ValueError:
                mp_next.append(0)
            try:
                min_next.append(int(re.sub(',', '', i.find('td', {'data-stat': 'minutes'}).text)))
            except ValueError:
                min_next.append(0)
            try:
                gls_next.append(int(re.sub(',', '', i.find('td', {'data-stat': 'goals'}).text)))
            except ValueError:
                gls_next.append(0)
            try:
                asst_next.append(int(re.sub(',', '', i.find('td', {'data-stat': 'assists'}).text)))
            except ValueError:
                asst_next.append(0)
            try:
                gls_asst_next.append(int(re.sub(',', '', i.find('td', {'data-stat': 'goals_assists'}).text)))
            except ValueError:
                gls_asst_next.append(0)
            next_stat_counter -= 1
        else:
            next_stat_counter -= 1

    while len(mp_next) < 2:
        mp_next.append('')
    while len(min_next) < 2:
        min_next.append('')
    while len(gls_next) < 2:
        gls_next.append('')
    while len(asst_next) < 2:
        asst_next.append('')
    while len(gls_asst_next) < 2:
        gls_asst_next.append('')
    
    time.sleep(3)       
    print('Análisis de carrera completo')

    return mp_next, min_next, gls_next, asst_next, gls_asst_next # (Temporadas en primera, máximo nivel de competencia)