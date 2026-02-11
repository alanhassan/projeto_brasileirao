import streamlit as st
import pandas as pd
import numpy as np
import os

# --- Configurações de Página ---
st.set_page_config(layout="wide", page_title="🏆 Visão Ranking - Classificação Detalhada")

# --- Variáveis Globais ---
FILE_PATH = 'df.xlsx' 

TEAM_LOGOS = {
    'Fortaleza Ec Saf': 'https://upload.wikimedia.org/wikipedia/commons/e/e9/Fortaleza_EC_2018.png',
    'Juventude': 'https://upload.wikimedia.org/wikipedia/de/c/cd/Juventude_logo.svg',
    'Cruzeiro Saf': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Cruzeiro_Esporte_Clube_%28logo%29.svg/250px-Cruzeiro_Esporte_Clube_%28logo%29.svg.png',
    'Vasco da Gama S.a.f.': 'https://upload.wikimedia.org/wikipedia/pt/thumb/8/8b/EscudoDoVascoDaGama.svg/950px-EscudoDoVascoDaGama.svg.png',
    'Grêmio': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Gremio_logo.svg/250px-Gremio_logo.svg.png',
    'Palmeiras': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Palmeiras_logo.svg/250px-Palmeiras_logo.svg.png',
    'Flamengo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Flamengo_braz_logo.svg/250px-Flamengo_braz_logo.svg.png',
    'Bahia': 'https://upload.wikimedia.org/wikipedia/pt/thumb/9/90/ECBahia.png/250px-ECBahia.png',
    'Botafogo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Botafogo_de_Futebol_e_Regatas_logo.svg/1064px-Botafogo_de_Futebol_e_Regatas_logo.svg.png',
    'São Paulo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Brasao_do_Sao_Paulo_Futebol_Clube.svg/1024px-Brasao_do_Sao_Paulo_Futebol_Clube.svg.png',
    'Corinthians': 'https://upload.wikimedia.org/wikipedia/pt/thumb/b/b4/Corinthians_simbolo.png/250px-Corinthians_simbolo.png',
    'Ceará': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Cear%C3%A1_Sporting_Club_logo.svg/1081px-Cear%C3%A1_Sporting_Club_logo.svg.png',
    'Red Bull Bragantino': 'https://upload.wikimedia.org/wikipedia/pt/thumb/9/9e/RedBullBragantino.png/250px-RedBullBragantino.png',
    'Internacional': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/SC_Internacional_Brazil_Logo.svg/250px-SC_Internacional_Brazil_Logo.svg.png',
    'Sport Recife': 'https://upload.wikimedia.org/wikipedia/pt/1/17/Sport_Club_do_Recife.png',
    'Mirassol': 'https://upload.wikimedia.org/wikipedia/commons/5/5b/Mirassol_FC_logo.png',
    'Atlético Mineiro Saf': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Atletico_mineiro_galo.png/250px-Atletico_mineiro_galo.png',
    'Santos Fc': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Santos_logo.svg/1045px-Santos_logo.svg.png',
    'Fluminense': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Fluminense_Football_Club.svg/250px-Fluminense_Football_Club.svg.png',
    'Vitória': 'https://upload.wikimedia.org/wikipedia/pt/3/34/Esporte_Clube_Vit%C3%B3ria_logo.png'
}

@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"Erro: O arquivo `{file_path}` não foi encontrado.")
        return pd.DataFrame() 
    try:
        df = pd.read_excel(file_path)
        df['Ordem_Jogo'] = df['Ordem_Jogo'].astype(int)
        df['Posicao_Jogo'] = df['Posicao_Jogo'].astype(int)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()

# --- Funções de Cálculo ---

def calculate_team_metrics(df, team_name, selected_year, local_filter=None):
    """Calcula as métricas filtrando por Time, Ano e Local."""
    # Filtro Primário: Time e Ano
    df_team = df[(df['Time1'] == team_name) & (df['Ano'] == selected_year)].copy() 
    
    df_team.drop_duplicates(subset=['Ordem_Jogo'], keep='first', inplace=True) 
    
    if df_team.empty:
        return {'P': 0, 'J': 0, 'V': 0, 'E': 0, 'D': 0, 'GM': 0, 'GC': 0, 'SG': 0, 'AP': 0.0, 'GPJ': 0.0, 'PPJ': 0.0}

    # GS, GC e Pontos
    df_team['GS'] = df_team.apply(lambda row: row['Gols1'] if row['Time1'] == team_name else row['Gols2'], axis=1)
    df_team['GC'] = df_team.apply(lambda row: row['Gols2'] if row['Time1'] == team_name else row['Gols1'], axis=1)
    df_team['Pontos_Jogo'] = df_team['Resultado'].map({'V': 3, 'E': 1, 'D': 0})
    
    # Filtro opcional de Local
    if local_filter:
        df_team = df_team[df_team['Local'] == local_filter]

    if df_team.empty:
        return {'P': 0, 'J': 0, 'V': 0, 'E': 0, 'D': 0, 'GM': 0, 'GC': 0, 'SG': 0, 'AP': 0.0, 'GPJ': 0.0, 'PPJ': 0.0}

    total_games = len(df_team)
    total_points = df_team['Pontos_Jogo'].sum()
    total_gm = df_team['GS'].sum()
    total_gc = df_team['GC'].sum()
    
    results_count = df_team['Resultado'].value_counts().to_dict()

    return {
        'P': total_points,
        'J': total_games,
        'V': results_count.get('V', 0),
        'E': results_count.get('E', 0),
        'D': results_count.get('D', 0),
        'GM': total_gm,
        'GC': total_gc,
        'SG': total_gm - total_gc,
        'AP': (total_points / (total_games * 3)) * 100,
        'GPJ': total_gm / total_games,
        'PPJ': total_points / total_games
    }

def create_ranking_dataframe(df, all_teams, selected_year, local_filter=None):
    ranking_list = []
    for team in all_teams:
        metrics = calculate_team_metrics(df, team, selected_year, local_filter)
        metrics['Time'] = team
        ranking_list.append(metrics)
        
    ranking_df = pd.DataFrame(ranking_list)
    # Filtra times que não tiveram jogos no ano/local selecionado para não poluir o ranking
    ranking_df = ranking_df[ranking_df['J'] > 0]
    
    return ranking_df

def add_logo_html(team_name, position):
    logo_url = TEAM_LOGOS.get(team_name, 'https://placehold.co/20x20/cccccc/333333?text=?')
    return f"""
    <div style="display: flex; align-items: center; white-space: nowrap;">
        <span style="font-weight: bold; width: 30px;">{position}</span> 
        <img src="{logo_url}" style="width: 20px; height: 20px; margin-right: 8px; object-fit: contain;">
        <span>{team_name}</span>
    </div>
    """

# --- Execução Principal ---

df = load_data(FILE_PATH)

if df.empty:
    st.warning("Dados não carregados.")
    st.stop()
    
all_teams = pd.unique(df[['Time1', 'Time2']].values.ravel('K'))
all_teams.sort()

# Título e Filtros
st.title("🏆 Visão Ranking - Classificação Detalhada")
st.markdown("---")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    ranking_option = st.selectbox(
        "Tipo de Ranking:",
        ('Classificação (Pontos)', 'Melhor Ataque (GM)', 'Melhor Defesa (GC)', 'Média de Pontos (PPJ)', 'Média de Gols (GPJ)')
    )

with col2:
    local_display = st.radio("Local:", ('Geral', 'Casa', 'Fora'), horizontal=True)
    local_filter = {'Geral': None, 'Casa': 'C', 'Fora': 'F'}[local_display]

with col3:
    all_years = sorted(df['Ano'].unique().tolist(), reverse=True)
    selected_year = st.selectbox("Ano:", all_years)

# Processamento do Ranking
ranking_df = create_ranking_dataframe(df, all_teams, selected_year, local_filter)

# Ordenação lógica
if 'Pontos' in ranking_option:
    sort_cols, ascending = ['P', 'V', 'SG', 'GM'], [False, False, False, False]
    title = f"Classificação Geral - {selected_year} ({local_display})"
elif 'Ataque' in ranking_option:
    sort_cols, ascending = ['GM', 'V', 'SG', 'P'], [False, False, False, False]
    title = f"Melhores Ataques - {selected_year} ({local_display})"
elif 'Defesa' in ranking_option:
    sort_cols, ascending = ['GC', 'SG', 'V', 'P'], [True, False, False, False]
    title = f"Melhores Defesas - {selected_year} ({local_display})"
elif 'PPJ' in ranking_option:
    sort_cols, ascending = ['PPJ', 'V', 'SG', 'P'], [False, False, False, False]
    title = f"Média de Pontos por Jogo - {selected_year} ({local_display})"
else: # GPJ
    sort_cols, ascending = ['GPJ', 'V', 'SG', 'P'], [False, False, False, False]
    title = f"Média de Gols por Jogo - {selected_year} ({local_display})"

ranking_df = ranking_df.sort_values(by=sort_cols, ascending=ascending).reset_index(drop=True)

# Preparação para exibição
st.subheader(title)

if not ranking_df.empty:
    ranking_df['Pos'] = ranking_df.index + 1
    ranking_df['Pos | Time'] = ranking_df.apply(lambda row: add_logo_html(row['Time'], row['Pos']), axis=1)

    cols_to_show = ['Pos | Time', 'P', 'J', 'V', 'E', 'D', 'GM', 'GC', 'SG', 'PPJ', 'GPJ', 'AP']
    rename_map = {'P': 'Pts', 'J': 'J', 'AP': 'Aprv %'}

    styled_df = ranking_df[cols_to_show].rename(columns=rename_map).style.format({
        'PPJ': "{:.2f}",
        'GPJ': "{:.2f}",
        'Aprv %': "{:.1f}%"
    })

    st.markdown(styled_df.hide(axis='index').to_html(escape=False), unsafe_allow_html=True)
else:
    st.info(f"Sem dados para os filtros selecionados em {selected_year}.")

st.markdown("---")
st.markdown("""
**Legenda:** **Pts:** Pontos | **J:** Jogos | **V/E/D:** Vitórias/Empates/Derrotas | **GM:** Gols Marcados | **GC:** Gols Sofridos | **SG:** Saldo | **PPJ:** Pontos/Jogo | **GPJ:** Gols/Jogo | **Aprv:** Aproveitamento.
""")

st.markdown("<p style='text-align: center; color: gray;'>Dashboard de Análise | Alan W. Hassan</p>", unsafe_allow_html=True)