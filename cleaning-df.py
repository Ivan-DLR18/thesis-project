import pandas as pd
from data_collection_utils import *

# Change accordingly
fbref_df = pd.read_csv('ENG-fbref.csv')
main_df = pd.read_csv('player-dataset-complete-v3.csv')
markt_val_df = pd.read_csv('ENG-market-value.csv')
attributes_df = pd.read_csv('ENG-attributes.csv')

# FBREF
fbref_df['player'] = fbref_df['player'].str.lower()
fbref_df = fbref_df.groupby(['player_link']).agg({ # Agrupa los repetidos usando su link sumando los minutos jugados, los partidos, goles, ast, etc.
    'player': 'first',
    'Nation': 'first',
    'Pos': 'first',
    'team': ' | '.join,
    'age': 'first',
    'MP': 'sum',
    'Min': 'sum',
    'Gls': 'sum',
    'Ast': 'sum',
    'G+A': 'sum',
    'elite_bool': 'first',
    'elite_num': 'first'
}).reset_index()
fbref_df['player'] = fbref_df['player'].apply(normalize_names)
fbref_df['team'] = fbref_df['team'].apply(normalize_names)
fbref_df.to_csv('FRA-fbref.csv', index=False)



# TRANSFERMARKT
markt_val_df['team'] = markt_val_df['team'].apply(sub_team)
markt_val_df['team'] = markt_val_df['team'].apply(normalize_names)
markt_val_df['player'] = markt_val_df['player'].apply(normalize_names)
markt_val_df.to_csv('FRA-market-value.csv', index=False)

# SOFIFA
attributes_df = attributes_df.rename(columns={'name': 'player'})
attributes_df['team'] = attributes_df['team'].apply(sub_team)
attributes_df['team'] = attributes_df['team'].apply(normalize_names)
attributes_df['player'] = attributes_df['player'].apply(normalize_names)
attributes_df['player'] = attributes_df['player'].str.lower()
attributes_df['player'] = attributes_df['player'].apply(second_lastname_erase)
attributes_df.to_csv('FRA-attributes.csv', index=False)


print(fbref_df.head())
print(markt_val_df.head())
print(attributes_df.head())

merged_df = pd.merge(fbref_df, markt_val_df, on=['player', 'team'], how='outer')
merged_df = pd.merge(merged_df, attributes_df, on=['player', 'team'], how='outer')
merged_df = pd.merge(main_df, attributes_df, on=['team', 'overall', 'potential', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physical'], how='outer')
merged_df.to_csv('FRA-merged-test.csv', index=False)


## Standarizing merged df as needed

# player_df = pd.read_csv('ESP-merged.csv')
# print(player_df.columns)

# aggregated_df = player_df.groupby(['player_link']).agg({
#     'player': 'first', 
#     'Nation': 'first', 
#     'Pos': 'first', 
#     'team': ' | '.join,
#     'age_x': 'first',
#     'MP': 'sum', 
#     'Min': 'sum', 
#     'Gls': 'sum', 
#     'Ast': 'sum',
#     'G+A': 'sum', 
#     'elite_bool': 'first', 
#     'elite_num': 'first',
#     'initial_value': select_first_non_missing, 
#     'max_value': select_first_non_missing,
#     'overall': select_first_non_missing, 
#     'potential': select_first_non_missing, 
#     'pace': select_first_non_missing,
#     'shooting': select_first_non_missing, 
#     'passing': select_first_non_missing, 
#     'dribbling': select_first_non_missing, 
#     'defending': select_first_non_missing, 
#     'physical': select_first_non_missing
# }).reset_index()

# # Print the aggregated DataFrame
# print(aggregated_df)
# aggregated_df.to_csv('ESP-player-dataset.csv')