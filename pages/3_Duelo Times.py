import streamlit as st
import pandas as pd
import numpy as np
import os

# --- Configurações de Página ---
st.set_page_config(layout="wide", page_title="⚔️ Duelo Times - Análise Comparativa")

# --- Variáveis Globais ---
FILE_PATH = 'df_final.xlsx' 

TEAM_LOGOS = {
    'Fortaleza Ec': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Fortaleza_Esporte_Clube_logo.png/640px-Fortaleza_Esporte_Clube_logo.png',
    'Juventude': 'https://upload.wikimedia.org/wikipedia/de/c/cd/Juventude_logo.svg',
    'Cruzeiro': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Cruzeiro_Esporte_Clube_%28logo%29.svg/250px-Cruzeiro_Esporte_Clube_%28logo%29.svg.png',
    'Vasco da Gama': 'https://upload.wikimedia.org/wikipedia/pt/thumb/8/8b/EscudoDoVascoDaGama.svg/950px-EscudoDoVascoDaGama.svg.png',
    'Grêmio': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Gremio_logo.svg/250px-Gremio_logo.svg.png',
    'Palmeiras': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Palmeiras_logo.svg/250px-Palmeiras_logo.svg.png',
    'Flamengo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Clube_de_Regatas_do_Flamengo_logo.svg/640px-Clube_de_Regatas_do_Flamengo_logo.svg.png',
    'Bahia': 'https://upload.wikimedia.org/wikipedia/pt/thumb/9/90/ECBahia.png/250px-ECBahia.png',
    'Botafogo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Botafogo_de_Futebol_e_Regatas_logo.svg/1064px-Botafogo_de_Futebol_e_Regatas_logo.svg.png',
    'São Paulo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Brasao_do_Sao_Paulo_Futebol_Clube.svg/1024px-Brasao_do_Sao_Paulo_Futebol_Clube.svg.png',
    'Corinthians': 'https://upload.wikimedia.org/wikipedia/pt/thumb/b/b4/Corinthians_simbolo.png/250px-Corinthians_simbolo.png',
    'Ceará': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Cear%C3%A1_Sporting_Club_logo.svg/1081px-Cear%C3%A1_Sporting_Club_logo.svg.png',
    'Red Bull Bragantino': 'https://upload.wikimedia.org/wikipedia/pt/thumb/9/9e/RedBullBragantino.png/250px-RedBullBragantino.png',
    'Internacional': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Sport_Club_Internacional_logo.svg/640px-Sport_Club_Internacional_logo.svg.png',
    'Sport Recife': 'https://upload.wikimedia.org/wikipedia/pt/1/17/Sport_Club_do_Recife.png',
    'Mirassol': 'https://upload.wikimedia.org/wikipedia/commons/5/5b/Mirassol_FC_logo.png',
    'Atlético Mineiro': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Atletico_mineiro_galo.png/250px-Atletico_mineiro_galo.png',
    'Santos Fc': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Santos_logo.svg/1045px-Santos_logo.svg.png',
    'Fluminense': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Fluminense_Football_Club.svg/250px-Fluminense_Football_Club.svg.png',
    'Vitória': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Esporte_Clube_Vit%C3%B3ria.png/640px-Esporte_Clube_Vit%C3%B3ria.png',
    'Chapecoense': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/S%C3%ADmbolo_Chapecoense_sem_estrelas.svg/640px-S%C3%ADmbolo_Chapecoense_sem_estrelas.svg.png',
    'Athletico Paranaense': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Athletico_Paranaense_%28Logo_2019%29.svg/640px-Athletico_Paranaense_%28Logo_2019%29.svg.png',
    'Coritiba': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Coritiba_Foot_Ball_Club_logo.svg/640px-Coritiba_Foot_Ball_Club_logo.svg.png',
    'Remo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Clube_do_Remo.svg/640px-Clube_do_Remo.svg.png',
}

@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"Erro: Arquivo não encontrado: `{file_path}`.")
        return pd.DataFrame() 
    try:
        df = pd.read_excel(file_path)
        df['Ordem_Jogo'] = df['Ordem_Jogo'].astype(int)
        df['Posicao_Jogo'] = df['Posicao_Jogo'].astype(int)
        return df
    except Exception as e:
        st.error(f"Erro ao processar Excel: {e}")
        return pd.DataFrame()

def get_recent_performance(df, team_name, local_filter=None, n_games=3):
    df_team = df[(df['Time1'] == team_name)].copy()
    df_team.drop_duplicates(subset=['Ordem_Jogo'], keep='first', inplace=True)
    if local_filter:
        df_team = df_team[df_team['Local'] == local_filter]
    df_recent = df_team.sort_values(by='Ordem_Jogo', ascending=False).head(n_games)

    if df_recent.empty:
        return {'V': 0, 'E': 0, 'D': 0, 'P': 0, 'AP': 0.0, 'Results': []}

    total_games = len(df_recent)
    results_count = df_recent['Resultado'].value_counts().to_dict()
    victories = results_count.get('V', 0)
    draws = results_count.get('E', 0)
    total_points = (victories * 3) + (draws * 1)
    aproveitamento = (total_points / (total_games * 3)) * 100 if total_games > 0 else 0
    
    return {
        'V': victories, 'E': draws, 'D': results_count.get('D', 0),
        'P': total_points, 'AP': aproveitamento, 'Results': df_recent['Resultado'].tolist()
    }

def calculate_team_metrics(df, team_name, local_filter=None):
    df_team = df[(df['Time1'] == team_name)].copy() 
    df_team.drop_duplicates(subset=['Ordem_Jogo'], keep='first', inplace=True) 
    
    df_team['GS'] = df_team['Gols1']
    df_team['GC'] = df_team['Gols2']
    df_team['Saldo_Jogo'] = df_team['GS'] - df_team['GC']
    df_team['Pontos_Jogo'] = df_team['Resultado'].map({'V': 3, 'E': 1, 'D': 0})
    
    if local_filter:
        df_team = df_team[df_team['Local'] == local_filter]

    if df_team.empty:
        return {'P': 0, 'J': 0, 'V': 0, 'E': 0, 'D': 0, 'GM': 0, 'GC': 0, 'SG': 0, 'AP': 0.0, 'GPJ': 0.0, 'PPJ': 0.0, 'RECENT': get_recent_performance(df, team_name, local_filter)}

    total_games = len(df_team)
    total_points = df_team['Pontos_Jogo'].sum()
    total_gm = df_team['GS'].sum()
    results_count = df_team['Resultado'].value_counts().to_dict()
    
    return {
        'P': total_points, 'J': total_games, 'V': results_count.get('V', 0),
        'E': results_count.get('E', 0), 'D': results_count.get('D', 0),
        'GM': total_gm, 'GC': df_team['GC'].sum(), 'SG': df_team['Saldo_Jogo'].sum(),
        'AP': (total_points / (total_games * 3)) * 100,
        'GPJ': total_gm / total_games, 'PPJ': total_points / total_games,
        'RECENT': get_recent_performance(df, team_name, local_filter)
    }

def create_ranking_dataframe(df, all_teams):
    ranking_list = []
    for team in all_teams:
        metrics = calculate_team_metrics(df, team)
        metrics['Time'] = team
        ranking_list.append(metrics)
    ranking_df = pd.DataFrame(ranking_list)
    ranking_df = ranking_df.sort_values(by=['P', 'V', 'SG', 'GM'], ascending=False).reset_index(drop=True)
    ranking_df.index = ranking_df.index + 1
    return ranking_df

def display_team_header(team_name, role):
    logo_url = TEAM_LOGOS.get(team_name, 'https://placehold.co/50x50/cccccc/333333?text=?')
    st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <img src="{logo_url}" style="width: 50px; height: 50px; margin-right: 15px; border-radius: 5px; object-fit: contain;">
            <div>
                <h3 style="margin: 0; padding: 0;">{team_name}</h3>
                <p style="margin: 0; padding: 0; font-style: italic; color: #888;">{role}</p>
            </div>
        </div>
        <hr style="margin-top: 0; margin-bottom: 20px;">
    """, unsafe_allow_html=True)

def display_metrics(metrics, current_pos, df_head_to_head, team_name):
    if metrics['J'] == 0:
        st.warning("Sem jogos no filtro selecionado.")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Colocação Atual (No Ano)", value=current_pos)
        st.metric(label=f"Aproveitamento ({metrics['J']} J)", value=f"{metrics['AP']:.1f}%")
        st.metric(label="Pontos por Jogo (PPJ)", value=f"{metrics['PPJ']:.1f}")
    with col2:
        st.metric(label="GM / Jogo", value=f"{metrics['GPJ']:.1f}")
        st.metric(label="GC / Jogo", value=f"{(metrics['GC']/metrics['J']):.1f}")
        st.metric(label="Saldo de Gols (SG)", value=f"{metrics['SG']}")

    st.markdown("#### Resultados (V/E/D) no Local:")
    st.markdown(f"""<span style="color:#28a745;"><b>{metrics['V']} V</b></span>, <b>{metrics['E']} E</b>, <span style="color:#dc3545;"><b>{metrics['D']} D</b></span>""", unsafe_allow_html=True)

    st.markdown("---")
    recent = metrics['RECENT']
    st.markdown(f"#### Últimos {len(recent['Results'])} Jogos (No Local):")
    result_emojis = {'V': '<span style="color:#28a745; font-size:20px;">●</span>', 'E': '<span style="color:#6c757d; font-size:20px;">●</span>', 'D': '<span style="color:#dc3545; font-size:20px;">●</span>'}
    results_html = " ".join([result_emojis.get(r, '⚪') for r in recent['Results'][::-1]])
    st.markdown(f"{results_html} (Antigo -> Recente)", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"#### Histórico Geral contra Adversário:")
    if not df_head_to_head.empty:
        for _, row in df_head_to_head.iterrows():
            if row['Time1'] == team_name:
                score = f"{row['Gols1']} x {row['Gols2']}"
                res = 'V' if row['Gols1'] > row['Gols2'] else 'D' if row['Gols1'] < row['Gols2'] else 'E'
            else:
                score = f"{row['Gols2']} x {row['Gols1']}"
                res = 'V' if row['Gols2'] > row['Gols1'] else 'D' if row['Gols2'] < row['Gols1'] else 'E'
            
            color = "#28a745" if res == 'V' else "#dc3545" if res == 'D' else "#000000"
            st.markdown(f'<span style="color:{color};"><b>{score}</b></span> - Jogo {row["Ordem_Jogo"]} ({row["Local"]}) - Ano {row["ano"]}', unsafe_allow_html=True)
    else:
        st.info("Nenhum confronto histórico encontrado.")

# --- Lógica Principal ---
df_full = load_data(FILE_PATH)
if df_full.empty:
    st.stop()

# Filtro de Ano na Sidebar
st.sidebar.header("Filtros de Visão")
anos_disponiveis = sorted(df_full['ano'].unique(), reverse=True)
ano_selecionado = st.sidebar.selectbox("Selecione o Ano para Estatísticas:", anos_disponiveis)

# DataFrame Filtrado para Métricas
df_filtrado = df_full[df_full['ano'] == ano_selecionado].copy()

all_teams = sorted(pd.unique(df_full[['Time1', 'Time2']].values.ravel('K')))
ranking_geral = create_ranking_dataframe(df_filtrado, all_teams)

st.title("⚔️ Duelo Times: Análise Comparativa")
st.markdown(f"**Analisando temporada: {ano_selecionado}** (Histórico de confrontos mostra todos os anos)")
st.markdown("---")

col_t1, col_t2 = st.columns(2)
team1_name = col_t1.selectbox("Time da Casa (Time 1):", all_teams, index=0)
team2_name = col_t2.selectbox("Time Visitante (Time 2):", all_teams, index=1 if len(all_teams)>1 else 0)

# Cálculos (Usando DF Filtrado por ano)
metrics_t1 = calculate_team_metrics(df_filtrado, team1_name, local_filter='C')
pos_t1 = ranking_geral.loc[ranking_geral['Time'] == team1_name].index[0] if not ranking_geral[ranking_geral['Time'] == team1_name].empty else 'N/A'

metrics_t2 = calculate_team_metrics(df_filtrado, team2_name, local_filter='F')
pos_t2 = ranking_geral.loc[ranking_geral['Time'] == team2_name].index[0] if not ranking_geral[ranking_geral['Time'] == team2_name].empty else 'N/A'

# Histórico (Usando DF FULL - Ignora o filtro de ano)
df_h2h_full = df_full[
    ((df_full['Time1'] == team1_name) & (df_full['Time2'] == team2_name)) |
    ((df_full['Time1'] == team2_name) & (df_full['Time2'] == team1_name))
].sort_values(by=['ano', 'Ordem_Jogo'], ascending=False)

# Exibição
col_disp1, col_vs, col_disp2 = st.columns([2, 0.5, 2])

with col_disp1:
    display_team_header(team1_name, "Mandante")
    display_metrics(metrics_t1, pos_t1, df_h2h_full, team1_name)

with col_vs:
    st.markdown("<h1 style='text-align: center; margin-top: 100px;'>VS</h1>", unsafe_allow_html=True)

with col_disp2:
    display_team_header(team2_name, "Visitante")
    display_metrics(metrics_t2, pos_t2, df_h2h_full, team2_name)

st.markdown("<br><hr><p style='text-align: center; color: gray;'>Dashboard de Análise de Performance | Autoria de Alan W. Hassan</p>", unsafe_allow_html=True)