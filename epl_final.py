import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("D:/PyProjetos/pjt004/epl/epl_final.csv", encoding='utf-8')

# Criar uma lista com todos os times de cada partida e seus resultados
def calcular_pontos(row):
    home_team = row['HomeTeam']
    away_team = row['AwayTeam']
    home_goals = row['FullTimeHomeGoals']
    away_goals = row['FullTimeAwayGoals']
    season = row['Season']

    if home_goals > away_goals:
        return [(season, home_team, 3), (season, away_team, 0)]
    elif home_goals < away_goals:
        return [(season, home_team, 0), (season, away_team, 3)]
    else:
        return [(season, home_team, 1), (season, away_team, 1)]

# Arsenal em casa
arsenal_home = df[df['HomeTeam'] == 'Arsenal'][[
    'Season', 'HomeShots', 'HomeShotsOnTarget', 'HomeCorners', 'HomeFouls', 'HomeYellowCards'
]]
# Renomear colunas para padronizar
arsenal_home.columns = ['Season', 'Shots', 'ShotsOnTarget', 'Corners', 'Fouls', 'YellowCards']

# Arsenal fora
arsenal_away = df[df['AwayTeam'] == 'Arsenal'][[
    'Season', 'AwayShots', 'AwayShotsOnTarget', 'AwayCorners', 'AwayFouls', 'AwayYellowCards'
]]
# Renomear colunas
arsenal_away.columns = ['Season', 'Shots', 'ShotsOnTarget', 'Corners', 'Fouls', 'YellowCards']

# Juntar casa e fora
arsenal_all = pd.concat([arsenal_home, arsenal_away])

# Média por temporada (casa + fora)
arsenal_grouped = arsenal_all.groupby('Season').mean().reset_index()

arsenal_grouped = arsenal_grouped[arsenal_grouped['Season'].between('2016/17', '2023/24')]

# Plot
plt.figure(figsize=(10,6))
plt.plot(arsenal_grouped['Season'], arsenal_grouped['Shots'], label='Chutes')
plt.plot(arsenal_grouped['Season'], arsenal_grouped['ShotsOnTarget'], label='Chutes no Gol')
plt.xticks(rotation=45)
plt.title('Arsenal - Evolução dos Chutes (Casa + Fora)')
plt.xlabel('Temporada')
plt.ylabel('Média por Jogo')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Manchester City em casa
city_home = df[df['HomeTeam'] == 'Man City'][[
    'Season', 'HomeShots', 'HomeShotsOnTarget', 'HomeCorners', 'HomeFouls', 'HomeYellowCards'
]]
city_home.columns = ['Season', 'Shots', 'ShotsOnTarget', 'Corners', 'Fouls', 'YellowCards']

# Manchester City fora
city_away = df[df['AwayTeam'] == 'Man City'][[
    'Season', 'AwayShots', 'AwayShotsOnTarget', 'AwayCorners', 'AwayFouls', 'AwayYellowCards'
]]
city_away.columns = ['Season', 'Shots', 'ShotsOnTarget', 'Corners', 'Fouls', 'YellowCards']

# Juntar casa e fora
city_all = pd.concat([city_home, city_away])

# Média por temporada (casa + fora)
city_grouped = city_all.groupby('Season').mean().reset_index()

# Filtro de temporadas entre 2015/16 e 2024/25
city_grouped = city_grouped[city_grouped['Season'].between('2013/14', '2023/24')]

# Plot
plt.figure(figsize=(10,6))
plt.plot(city_grouped['Season'], city_grouped['Shots'], label='Chutes')
plt.plot(city_grouped['Season'], city_grouped['ShotsOnTarget'], label='Chutes no Gol')
plt.xticks(rotation=45)
plt.title('Manchester City - Evolução dos Chutes (Casa + Fora)')
plt.xlabel('Temporada')
plt.ylabel('Média por Jogo')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot específico de faltas cometidas
plt.figure(figsize=(10,6))
plt.plot(city_grouped['Season'], city_grouped['Fouls'], color='red', marker='o')
plt.xticks(rotation=45)
plt.title('Manchester City - Faltas Cometidas por Temporada (Casa + Fora)')
plt.xlabel('Temporada')
plt.ylabel('Média de Faltas por Jogo')
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot específico de cartões amarelos
plt.figure(figsize=(10,6))
plt.plot(city_grouped['Season'], city_grouped['YellowCards'], color='gold', marker='o')
plt.xticks(rotation=45)
plt.title('Manchester City - Cartões Amarelos por Temporada (Casa + Fora)')
plt.xlabel('Temporada')
plt.ylabel('Média de Cartões Amarelos por Jogo')
plt.grid(True)
plt.tight_layout()
plt.show()

# Aplicar a função calcular_pontos a todas as linhas do DataFrame
todos_pontos = df.apply(calcular_pontos, axis=1)

# Achatar a lista de listas
todos_pontos_flat = [item for sublist in todos_pontos for item in sublist]

# Criar DataFrame com colunas: Season, Team, Points
tabela_pontos = pd.DataFrame(todos_pontos_flat, columns=['Season', 'Team', 'Points'])

# Somar os pontos por temporada e time
tabela_pontos = tabela_pontos.groupby(['Season', 'Team'])['Points'].sum().reset_index()

# Ordenar por temporada e pontos
tabela_pontos = tabela_pontos.sort_values(['Season', 'Points'], ascending=[True, False])

# Adicionar a posição (rank) de cada time por temporada
tabela_pontos['Position'] = tabela_pontos.groupby('Season')['Points'].rank(method='first', ascending=False)

# Filtrar apenas o Arsenal
arsenal_posicao = tabela_pontos[tabela_pontos['Team'] == 'Arsenal'].copy()

# Filtrar apenas as temporadas desejadas
arsenal_posicao = arsenal_posicao[arsenal_posicao['Season'].between('2016/17', '2023/24')]

# Plot
plt.figure(figsize=(10,6))
plt.plot(arsenal_posicao['Season'], arsenal_posicao['Position'], marker='o', linestyle='-', color='crimson')
plt.gca().invert_yaxis()  # 1º lugar no topo

# Estilizar
plt.title('Evolução da Posição do Arsenal na Premier League (2016/17 – 2023/24)', fontsize=14)
plt.xlabel('Temporada')
plt.ylabel('Posição na Tabela')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=1)
plt.tight_layout()
plt.show()

# Ordenar por temporada e pontos
tabela_pontos = tabela_pontos.sort_values(['Season', 'Points'], ascending=[True, False])

# Adicionar posição por temporada
tabela_pontos['Position'] = tabela_pontos.groupby('Season')['Points'].rank(method='first', ascending=False)

# Filtrar apenas o Manchester City
city_posicao = tabela_pontos[tabela_pontos['Team'] == 'Man City'].copy()

# Filtrar temporadas desejadas
city_posicao = city_posicao[city_posicao['Season'].between('2013/14', '2023/24')]

# Plot
plt.figure(figsize=(10,6))
plt.plot(city_posicao['Season'], city_posicao['Position'], marker='o', linestyle='-', color='dodgerblue')
plt.gca().invert_yaxis()  # 1º lugar no topo

# Definir o eixo Y com ticks de 1 em 1
max_posicao = int(city_posicao['Position'].max())
plt.yticks(range(1, max_posicao + 1))

# Estilizar
plt.title('Evolução da Posição do Manchester City na Premier League (2013/14 – 2023/24)', fontsize=14)
plt.xlabel('Temporada')
plt.ylabel('Posição na Tabela')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=1)
plt.tight_layout()
plt.show()

