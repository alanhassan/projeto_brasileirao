import streamlit as st
import pandas as pd
import numpy as np
import os

# --- Configurações de Página ---
st.set_page_config(layout="wide", page_title="⚔️ Duelo Times - Análise Comparativa")

# --- Variáveis Globais (Ajuste o caminho se necessário) ---
FILE_PATH = 'df.xlsx' 

# Dicionário de Logos dos Times (REPLICADO)
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
    """Carrega os dados do Excel com tratamento de erros."""
    if not os.path.exists(file_path):
          st.error(f"Erro: O arquivo não foi encontrado no caminho especificado: `{file_path}`.")
          return pd.DataFrame() 
    
    try:
        df = pd.read_excel(file_path)
        # Conversão de tipos importantes
        df['Ordem_Jogo'] = df['Ordem_Jogo'].astype(int)
        df['Posicao_Jogo'] = df['Posicao_Jogo'].astype(int)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar ou processar os dados do Excel: {e}. Verifique a estrutura do arquivo.")
        return pd.DataFrame()
    
# --- NOVO: Função para Desempenho Recente ---
def get_recent_performance(df, team_name, local_filter=None, n_games=3):
    """
    Calcula o desempenho nos últimos N jogos, com filtro opcional por Local.
    Retorna um dicionário com V, E, D, Pts, AP e uma lista com os resultados (V/E/D).
    """
    # 1. Filtra os jogos onde o time é Time1 (Time1 foi padronizado para o time em foco)
    df_team = df[(df['Time1'] == team_name)].copy()
    df_team.drop_duplicates(subset=['Ordem_Jogo'], keep='first', inplace=True)

    # 2. Aplica filtro de Local
    if local_filter:
        df_team = df_team[df_team['Local'] == local_filter]
        
    # 3. Ordena e pega os N jogos mais recentes
    # 'Ordem_Jogo' é a chave para o mais recente (maior valor)
    df_recent = df_team.sort_values(by='Ordem_Jogo', ascending=False).head(n_games)

    if df_recent.empty:
        return {'V': 0, 'E': 0, 'D': 0, 'P': 0, 'AP': 0.0, 'Results': []}

    total_games = len(df_recent)
    
    # 4. Resultados V/E/D
    results_count = df_recent['Resultado'].value_counts().to_dict()
    victories = results_count.get('V', 0)
    draws = results_count.get('E', 0)
    defeats = results_count.get('D', 0)
    
    # 5. Pontos e Aproveitamento
    total_points = (victories * 3) + (draws * 1)
    aproveitamento = (total_points / (total_games * 3)) * 100 if total_games > 0 else 0
    
    # 6. Lista dos resultados (para exibição)
    results_list = df_recent['Resultado'].tolist() # Lista de ['V', 'E', 'D']

    return {
        'V': victories,
        'E': draws,
        'D': defeats,
        'P': total_points,
        'AP': aproveitamento,
        'Results': results_list
    }


# --- Funções de Cálculo (Reutilizada da página anterior) ---

def calculate_team_metrics(df, team_name, local_filter=None):
    """
    Calcula as métricas de V/E/D, Gols Marcados/Sofridos, Pontos Acumulados 
    e as novas métricas GPJ e PPJ para um time, com filtro opcional por Local.
    """
    df_team = df[(df['Time1'] == team_name)].copy() 
    df_team.drop_duplicates(subset=['Ordem_Jogo'], keep='first', inplace=True) 
    
    # 1. Calcular GS, GC, Saldo, Pontos_Jogo
    df_team['GS'] = df_team.apply(
        lambda row: row['Gols1'] if row['Time1'] == team_name else row['Gols2'], axis=1
    )
    df_team['GC'] = df_team.apply(
        lambda row: row['Gols2'] if row['Time1'] == team_name else row['Gols1'], axis=1
    )
    df_team['Saldo_Jogo'] = df_team['GS'] - df_team['GC']
    df_team['Pontos_Jogo'] = df_team['Resultado'].map({'V': 3, 'E': 1, 'D': 0})
    
    if local_filter:
        df_team = df_team[df_team['Local'] == local_filter]

    # 2. Resumir as métricas
    if df_team.empty or len(df_team) == 0:
        return {
            'P': 0, 'J': 0, 'V': 0, 'E': 0, 'D': 0, 
            'GM': 0, 'GC': 0, 'SG': 0, 'AP': 0.0,
            'GPJ': 0.0, 'PPJ': 0.0
        }

    total_games = len(df_team)
    total_points = df_team['Pontos_Jogo'].sum()
    total_gm = df_team['GS'].sum()
    total_gc = df_team['GC'].sum()
    
    # Cálculos Avançados
    aproveitamento = (total_points / (total_games * 3)) * 100 if total_games > 0 else 0
    gols_por_jogo = total_gm / total_games if total_games > 0 else 0
    pontos_por_jogo = total_points / total_games if total_games > 0 else 0
    
    results_count = df_team['Resultado'].value_counts().to_dict()

    # NOVO: Cálculo do Desempenho Recente
    recent_performance = get_recent_performance(df, team_name, local_filter=local_filter, n_games=3)

    return {
        'P': total_points,
        'J': total_games,
        'V': results_count.get('V', 0),
        'E': results_count.get('E', 0),
        'D': results_count.get('D', 0),
        'GM': total_gm,
        'GC': total_gc,
        'SG': df_team['Saldo_Jogo'].sum(),
        'AP': aproveitamento,
        'GPJ': gols_por_jogo,
        'PPJ': pontos_por_jogo,
        'RECENT': recent_performance
    }

def create_ranking_dataframe(df, all_teams):
    """
    Cria um DataFrame de ranking GERAL para determinar a colocação atual.
    """
    ranking_list = []
    
    for team in all_teams:
        metrics = calculate_team_metrics(df, team)
        metrics['Time'] = team
        ranking_list.append(metrics)
        
    ranking_df = pd.DataFrame(ranking_list)
    
    # Ordenação padrão para Classificação Geral
    ranking_df = ranking_df.sort_values(
        by=['P', 'V', 'SG', 'GM'], 
        ascending=[False, False, False, False]
    ).reset_index(drop=True)
    
    ranking_df.index = ranking_df.index + 1 # Posição começando em 1
    ranking_df.index.name = 'Pos'
    
    return ranking_df

# --- Funções de Componentes Visuais ---

def display_team_header(team_name, role):
    """Exibe o logo e o nome do time com a função (Casa/Fora)."""
    logo_url = TEAM_LOGOS.get(team_name, 'https://placehold.co/50x50/cccccc/333333?text=?')
    
    # Renderiza o logo e o nome
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

def display_metrics(metrics, current_pos, df_head_to_head):
    """Exibe as métricas de desempenho e resultados contra o adversário."""
    if metrics['J'] == 0:
        st.warning("O time não possui jogos no filtro selecionado (Casa/Fora).")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Colocação Atual (Geral)", value=current_pos)
        st.metric(label=f"Aproveitamento ({metrics['J']} J)", value=f"{metrics['AP']:.1f}%")
        st.metric(label="Pontos por Jogo (PPJ)", value=f"{metrics['PPJ']:.1f}")
        
    with col2:
        st.metric(label="Gols Marcados / Jogo (GM/J)", value=f"{metrics['GPJ']:.1f}")
        gc_por_jogo = metrics['GC'] / metrics['J'] if metrics['J'] > 0 else 0
        st.metric(label="Gols Sofridos / Jogo (GC/J)", value=f"{gc_por_jogo:.1f}")
        st.metric(label="Saldo de Gols (SG)", value=f"{metrics['SG']}")

    st.markdown("#### Resultados (V/E/D) no Local Selecionado:")
    # Cores a serem usadas
    green_hex = "#28a745" # Verde para Vitórias
    red_hex = "#dc3545"   # Vermelho para Derrotas
    black_hex = "#000000" # Preto para Empates

    st.markdown(
        f"""
        <span style="color: {green_hex};"><b>{metrics['V']} Vitórias</b></span>, 
        <span style="color: {black_hex};"><b>{metrics['E']} Empates</b></span>, 
        <span style="color: {red_hex};"><b>{metrics['D']} Derrotas</b></span>.
        """, 
        unsafe_allow_html=True
    )

    st.markdown("---")
    # 2. NOVO: Exibição do Desempenho Recente
    recent = metrics['RECENT']
    
    num_recent_games = len(recent['Results'])
    st.markdown(f"#### Desempenho nos Últimos {num_recent_games} Jogos:")
    
    # Aproveitamento Recente
    st.markdown(f"**Aproveitamento:** **{recent['AP']:.1f}%**")

    # Contagem de V/E/D Recente
    st.markdown(
        f"""
        <span style="color: {green_hex};"><b>{recent['V']} V</b></span>,
        <span style="color: {black_hex};"><b>{recent['E']} E</b></span>,
        <span style="color: {red_hex};"><b>{recent['D']} D</b></span>
        """,
        unsafe_allow_html=True
    )
    
    # Sequência de Resultados (Visual)
    # Usamos pequenos círculos ou quadrados coloridos
    result_emojis = {
        'V': f'<span style="color: {green_hex}; font-size: 20px;">\u25CF</span>', # Círculo Verde
        'E': f'<span style="color: #6c757d; font-size: 20px;">\u25CF</span>', # Círculo Cinza (Empate)
        'D': f'<span style="color: {red_hex}; font-size: 20px;">\u25CF</span>' # Círculo Vermelho
    }
    
    # Inverte a lista para exibir do mais antigo para o mais recente para melhor leitura horizontal
    results_html = " ".join([result_emojis.get(r, '⚪') for r in recent['Results'][::-1]])
    st.markdown(f"**Sequência:** {results_html} (Antigo -> Recente)", unsafe_allow_html=True)


    st.markdown("---")

    # Resultados entre os times
    if not df_head_to_head.empty:
        st.markdown(f"#### Histórico de Jogos Contra o Adversário:")
        for _, row in df_head_to_head.iterrows():
            # Variáveis auxiliares
            gols_time1 = row['Gols1']
            gols_time2 = row['Gols2']
            local = row['Local']
            ordem_jogo = row['Ordem_Jogo']

            # Inicializa a string de placar e a cor
            score_text = ""
            color_hex = "" # Cor padrão para empate (preto)

            # Determina o resultado a partir da perspectiva do time principal (metrics['Time'])
            if row['Time1'] == metrics['Time']:
                score = f"{gols_time1} x {gols_time2}"
                if gols_time1 > gols_time2:
                    color_hex = "#28a745"  # Verde para vitória
                elif gols_time1 < gols_time2:
                    color_hex = "#dc3545"  # Vermelho para derrota
                else:
                    color_hex = "#000000"  # Preto para empate

            else: # Time2 é o time principal
                score = f"{gols_time2} x {gols_time1}"
                if gols_time2 > gols_time1:
                    color_hex = "#28a745"  # Verde para vitória
                elif gols_time2 < gols_time1:
                    color_hex = "#dc3545"  # Vermelho para derrota
                else:
                    color_hex = "#000000"  # Preto para empate

            # Formata o texto do resultado com a cor e negrito usando HTML/Markdown
            # Usamos <b> para negrito e o estilo de cor diretamente no span
            st.markdown(
                f'<span style="color: {color_hex};"><b>Resultado: {score} - Jogo {ordem_jogo} - Local {local}</b></span>', 
                unsafe_allow_html=True
            )

    else:
        st.markdown(f"#### Histórico de Jogos Contra o Adversário:")
        st.info("Nenhum jogo encontrado entre esses dois times na base de dados.")


# --- Lógica Principal da Página ---

# 1. Carregamento e Verificação de Dados
df = load_data(FILE_PATH)

if df.empty:
    st.warning("Não foi possível carregar os dados. Verifique o caminho do arquivo.")
    st.stop()
    
all_teams = pd.unique(df[['Time1', 'Time2']].values.ravel('K'))
all_teams.sort()

# Prepara o Ranking Geral para Colocação Atual
ranking_geral = create_ranking_dataframe(df, all_teams)


st.title("⚔️ Duelo Times: Análise Comparativa")
st.markdown("---")

# 2. Seleção dos Times
st.header("Selecione os Times para o Duelo")
col_t1, col_t2 = st.columns(2)

# Time 1 (Casa)
team1_name = col_t1.selectbox(
    "Time da Casa (Time 1):",
    all_teams,  
    index=0
)

# Time 2 (Fora)
# Garante que o time 2 não seja o mesmo que o time 1
filtered_teams = all_teams[all_teams != team1_name]
team2_name = col_t2.selectbox(
    "Time Visitante (Time 2):",
        all_teams,
    index=0
)

st.markdown("---")

# 3. Cálculo das Métricas e Preparação dos Dados

# Métricas Time 1 (Casa): Apenas jogos em CASA ('C')
metrics_t1_home = calculate_team_metrics(df, team1_name, local_filter='C')
metrics_t1_home['Time'] = team1_name # <-- ADICIONE A CHAVE 'Time' AQUI
pos_t1 = ranking_geral.loc[ranking_geral['Time'] == team1_name].index[0] if not ranking_geral[ranking_geral['Time'] == team1_name].empty else 'N/A'

# Métricas Time 2 (Fora): Apenas jogos FORA ('F')
metrics_t2_away = calculate_team_metrics(df, team2_name, local_filter='F')
metrics_t2_away['Time'] = team2_name # <-- ADICIONE A CHAVE 'Time' AQUI
pos_t2 = ranking_geral.loc[ranking_geral['Time'] == team2_name].index[0] if not ranking_geral[ranking_geral['Time'] == team2_name].empty else 'N/A'

# Histórico de Jogos entre os dois times
df_head_to_head = df[
    ((df['Time1'] == team1_name) & (df['Time2'] == team2_name)) 
    # | ((df['Time1'] == team2_name) & (df['Time2'] == team1_name))
].sort_values(by='Ordem_Jogo', ascending=False)


# 4. Exibição do Duelo
col_display_t1, col_vs, col_display_t2 = st.columns([2, 0.5, 2])

# --- Coluna Time 1 (Casa) ---
with col_display_t1:
    display_team_header(team1_name, "Joga em Casa")
    display_metrics(metrics_t1_home, pos_t1, 
                    df_head_to_head[(df_head_to_head['Time1'] == team1_name) | 
                                    (df_head_to_head['Time2'] == team1_name)])

# --- Coluna VS ---
with col_vs:
    st.markdown("<h1 style='text-align: center; margin-top: 100px;'>VS</h1>", unsafe_allow_html=True)

# --- Coluna Time 2 (Fora) ---
with col_display_t2:
    display_team_header(team2_name, "Joga Fora")
    display_metrics(metrics_t2_away, pos_t2, 
                    df_head_to_head[(df_head_to_head['Time1'] == team2_name) | 
                                    (df_head_to_head['Time2'] == team2_name)])