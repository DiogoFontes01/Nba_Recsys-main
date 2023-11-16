import pandas as pd

def fill_missing_values_with_mean(df):
    
    # Calcular médias por posição
    mean_weights = df.groupby('Pos')['Weight'].transform('mean')
    mean_heights = df.groupby('Pos')['Height'].transform('mean')
    
    # Preencher valores faltantes com médias correspondentes
    df['Weight'].fillna(mean_weights, inplace=True)
    df['Height'].fillna(mean_heights, inplace=True)
    
    
    #Printar medias correspondetes
    mean_weights_by_pos = df.groupby('Pos')['Weight'].mean()
    #print(mean_weights_by_pos)
    
    mean_heights_by_pos = df.groupby('Pos')['Height'].mean()
    #print(mean_heights_by_pos)
    
    return df

def convert_height_to_float(height_str):
    if pd.isna(height_str):
        return None

    feet, inches = height_str.split("'")
    # Remova qualquer caractere não numérico das polegadas (por exemplo, aspas duplas)
    inches = ''.join(filter(str.isdigit, inches))
    
    return float(f"{feet}.{inches}")

df_nba = pd.read_csv('datasets/original.csv')


# Separe os jogadores que jogaram em várias equipes, identificados por 'TOT'
players_with_totals = df_nba[df_nba['Tm'] == 'TOT']['Player'].unique()

# Para cada um desses jogadores, faremos o seguinte:
for player in players_with_totals:
    # Encontrar todas as entradas para esse jogador
    player_entries = df_nba[df_nba['Player'] == player]

    # Identificar todas as equipes que não são 'TOT'
    non_tot_teams = player_entries[player_entries['Tm'] != 'TOT']['Tm'].unique()
    
    # Se existir mais de uma equipe, escolher a primeira equipe como a equipe representativa
    if len(non_tot_teams) > 0:
        representative_team = non_tot_teams[0]
        # Encontrar a posição do jogador na equipe representativa
        representative_position = player_entries[(df_nba['Tm'] == representative_team)]['Pos'].values[0]
    else:
        # Se por algum motivo não houver uma equipe não-TOT (o que seria estranho), podemos definir um valor padrão
        representative_team = 'Unknown'
        representative_position = 'Unknown'

    # Atualize a equipe 'TOT' para a equipe representativa e a posição para a posição na equipe representativa para este jogador
    df_nba.loc[(df_nba['Player'] == player) & (df_nba['Tm'] == 'TOT'), 'Tm'] = representative_team
    df_nba.loc[(df_nba['Player'] == player) & (df_nba['Tm'] == representative_team), 'Pos'] = representative_position

    # Remova todas as outras entradas do jogador que não são 'TOT'
    df_nba = df_nba[~((df_nba['Player'] == player) & (df_nba['Tm'] != representative_team))]

df_nba.to_csv('datasets/nba_2022_2023.csv', index=False)

df_new = pd.read_csv('datasets/nba_2022_2023.csv')

df_new = df_new.drop_duplicates(subset=['Age', 'Player'], keep='first')

df_new.to_csv('datasets/nba_2022_2023.csv', index=False)

# add column salary to the dataframe from nbasal

df_salarios = pd.read_csv('datasets/nbasal.csv')

#df_salarios['Player'] = df_new['Player'].apply(lambda x: unic.unidecode(x))

# Fundir os dataframes com base na coluna 'Player'
df_final = df_new.merge(df_salarios, left_on='Player', right_on='Player', how='left')

# Renomear a coluna de salários para 'Salario_2022/2023'
df_final = df_final.rename(columns={'2022/2023': 'Salario_2022/2023'})

# Salvar o resultado de volta em um arquivo CSV
df_final.to_csv('datasets/nba_2022_2023_com_salarios.csv', index=False)

# remove collums from data set

df_nba  = pd.read_csv('datasets/nba_2022_2023_com_salarios.csv')

df_nba = df_nba.drop(['2023/2024','2024/2025','2024/2025.1', "Player Id"], axis=1)

df_nba.to_csv('datasets/nba_2022_2023_com_salarios.csv', index=False)

nome_da_coluna = 'Salario_2022/2023'  # Substitua 'nome_da_sua_coluna' pelo nome real da sua coluna

df_nba[nome_da_coluna].fillna("$1,017,784", inplace=True)

df_nba[nome_da_coluna] = df_nba[nome_da_coluna].replace({'\$': '', ',': ''}, regex=True).astype(int)

df_nba.to_csv('datasets/nba_2022_2023_com_salarios.csv', index=False)

df_nba2k23 = pd.read_csv('datasets/nba2k23_data.csv')

# Selecionar apenas as colunas 'name', 'weight' e 'height'
df_nba2k23 = df_nba2k23[['Name', 'Weight', 'Height']]

#change name of Name collums to Player

df_nba2k23 = df_nba2k23.rename(columns={'Name': 'Player'})

# Salvar o DataFrame resultante em um novo arquivo .csv
df_nba2k23.to_csv('datasets/alturas.csv', index=False)

# join alturas.csv with nba_2022_2023_com_salarios.csv comparing player collum

df_nba = pd.read_csv('datasets/nba_2022_2023_com_salarios.csv')

df_alturas = pd.read_csv('datasets/alturas.csv')

df_nba = df_nba.merge(df_alturas, left_on='Player', right_on='Player', how='left')

df_nba.to_csv('datasets/nba_2022_2023_com_salarios.csv', index=False)

df_nba = pd.read_csv('datasets/nba_2022_2023_com_salarios.csv')

df_nba['Height'] = df_nba['Height'].apply(convert_height_to_float)

df_nba.to_csv('datasets/nba_final.csv', index=False)

df_nba = pd.read_csv('datasets/nba_final.csv')

df_nba = fill_missing_values_with_mean(df_nba)

df_nba.to_csv('datasets/nba_final.csv', index=False)

# Lendo o arquivo CSV e preenchendo os valores ausentes com zero
df_nba = pd.read_csv('datasets/nba_final.csv')
df_nba.fillna(0, inplace=True)  # Preenche os valores NaN com zero

# Salvando o DataFrame de volta no arquivo CSV
df_nba.to_csv('datasets/nba_final.csv', index=False)