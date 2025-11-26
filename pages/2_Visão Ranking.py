import streamlit as st
import pandas as pd
import numpy as np
import os

# --- Configurações de Página (Mantenha a consistência) ---
st.set_page_config(layout="wide", page_title="🏆 Visão Ranking - Classificação Detalhada")

# --- Variáveis Globais (INCLUÍDAS NOVAMENTE PARA ESTA PÁGINA) ---
FILE_PATH = 'df.xlsx' 

# Dicionário de Logos dos Times (REPLICADO DA PÁGINA "VISÃO TIME")
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
    'Fluminense': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/FFC_crest.svg/1037px-FFC_crest.svg.png',
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

# --- Funções de Cálculo de Métricas por Time/Local (SEM ALTERAÇÃO) ---

def calculate_team_metrics(df, team_name, local_filter=None):
    """
    Calcula as métricas de V/E/D, Gols Marcados/Sofridos, Pontos Acumulados 
    e as novas métricas GPJ e PPJ para um time, com filtro opcional por Local.
    """
    df_team = df[(df['Time1'] == team_name) ].copy() 
    
    # Remove duplicatas se houver
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
    if df_team.empty:
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
    
    # Contagem de resultados
    results_count = df_team['Resultado'].value_counts().to_dict()

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
        'PPJ': pontos_por_jogo
    }

def create_ranking_dataframe(df, all_teams, local_filter=None):
    """
    Cria um DataFrame de ranking completo com as métricas calculadas.
    """
    ranking_list = []
    
    # Itera sobre todos os times e calcula as métricas
    for team in all_teams:
        metrics = calculate_team_metrics(df, team, local_filter)
        metrics['Time'] = team
        ranking_list.append(metrics)
        
    ranking_df = pd.DataFrame(ranking_list)
    
    # Ordenação padrão da tabela (Posição)
    ranking_df['AP'] = ranking_df['AP'].round(1) # Arredonda o aproveitamento
    ranking_df = ranking_df.sort_values(
        by=['P', 'V', 'SG', 'GM'], 
        ascending=[False, False, False, False]
    ).reset_index(drop=True)
    
    ranking_df.index = ranking_df.index + 1 # Posição começando em 1
    ranking_df.index.name = 'Pos'
    
    return ranking_df


# --- Layout da Página ---

# 1. Carregamento e Verificação de Dados
df = load_data(FILE_PATH)

if df.empty:
    st.warning("Não foi possível carregar os dados. Verifique o caminho do arquivo e se o Excel está fechado.")
    st.stop()
    
all_teams = pd.unique(df[['Time1', 'Time2']].values.ravel('K'))
all_teams.sort()


# 2. Título e Filtros
st.title("🏆 Visão Ranking - Classificação Detalhada")
st.markdown("---")

col_rank_sel, col_local_sel = st.columns(2)

# Filtro de Tipo de Ranking (ATUALIZADO com as novas opções)
ranking_option = col_rank_sel.selectbox(
    "Selecione o Tipo de Ranking:",
    ('Classificação (Pontos)', 
     'Melhor Ataque (Gols Marcados)', 
     'Melhor Defesa (Gols Sofridos)',
     'Média de Pontos por Jogo (PPJ)',
     'Média de Gols por Jogo (GPJ)'
     ),
    index=0
)

# Filtro de Local (Casa/Fora)
local_display = col_local_sel.radio(
    "Selecione a Visão por Local:",
    ('Geral', 'Casa', 'Fora'),
    index=0,
    horizontal=True
)

# Mapeamento do filtro de exibição para o filtro de cálculo
local_filter_map = {
    'Geral': None,
    'Casa': 'C',
    'Fora': 'F'
}
local_filter = local_filter_map[local_display]


# 3. Criação do DataFrame de Ranking com o filtro selecionado
ranking_df = create_ranking_dataframe(df, all_teams, local_filter)


# 4. Configuração da Ordenação de Acordo com a Opção Escolhida
if ranking_option == 'Classificação (Pontos)':
    title = f"Classificação por Pontos - Visão {local_display}"
    
elif ranking_option == 'Melhor Ataque (Gols Marcados)':
    ranking_df = ranking_df.sort_values(
        by=['GM', 'V', 'SG', 'P'], 
        ascending=[False, False, False, False]
    ).reset_index(drop=True)
    title = f"Ranking de Melhor Ataque (GM) - Visão {local_display}"

elif ranking_option == 'Melhor Defesa (Gols Sofridos)':
    ranking_df = ranking_df.sort_values(
        by=['GC', 'SG', 'V', 'P'], 
        ascending=[True, False, False, False] 
    ).reset_index(drop=True)
    title = f"Ranking de Melhor Defesa (GC) - Visão {local_display}"

elif ranking_option == 'Média de Pontos por Jogo (PPJ)': 
    ranking_df = ranking_df.sort_values(
        by=['PPJ', 'V', 'SG', 'P'], 
        ascending=[False, False, False, False]
    ).reset_index(drop=True)
    title = f"Ranking de Média de Pontos por Jogo (PPJ) - Visão {local_display}"

elif ranking_option == 'Média de Gols por Jogo (GPJ)': 
    ranking_df = ranking_df.sort_values(
        by=['GPJ', 'V', 'SG', 'P'], 
        ascending=[False, False, False, False]
    ).reset_index(drop=True)
    title = f"Ranking de Média de Gols por Jogo (GPJ) - Visão {local_display}"


ranking_df.index = ranking_df.index + 1
ranking_df.index.name = 'Pos'


# 5. Exibição do Ranking (ATUALIZADA PARA INCLUIR LOGO)
st.subheader(title)

# --- NOVO CÓDIGO PARA ADICIONAR LOGO ---

def add_logo_html(team_name, position):
    """Gera o HTML com o logo, a POSIÇÃO e o nome do time."""
    logo_url = TEAM_LOGOS.get(team_name, 'https://placehold.co/20x20/cccccc/333333?text=?')
    # O HTML agora inclui a posição (index.name)
    return f"""
    <div style="display: flex; align-items: center; white-space: nowrap;">
        <span style="font-weight: bold; width: 30px;">{position}</span> 
        <img src="{logo_url}" style="width: 20px; height: 20px; margin-right: 8px; object-fit: contain;">
        <span>{team_name}</span>
    </div>
    """

# 1. Cria a coluna 'Pos_Time_HTML' combinando Posição (índice) e HTML do Time
# reset_index() é necessário para transformar o índice 'Pos' em uma coluna de dados
ranking_df_display = ranking_df.reset_index()

# *** PONTO DE CORREÇÃO ***
# A coluna 'Pos' estava iniciando em 2. Recalculamos ela a partir do índice (0-based) do DataFrame
ranking_df_display['Pos'] = ranking_df_display.index + 1


# Aplica a função usando a coluna 'Pos' (agora 1-based) e 'Time'
ranking_df_display['Pos_Time_HTML'] = ranking_df_display.apply(
    lambda row: add_logo_html(row['Time'], row['Pos']), axis=1
)


# 2. Seleciona e Renomeia as colunas para exibição
columns_to_display = ['Pos_Time_HTML', 'P', 'J', 'PPJ', 'V', 'E', 'D', 'GM', 'GC', 'SG', 'GPJ', 'AP']
column_names = {
    'Pos_Time_HTML': 'Pos | Time', # Novo cabeçalho combinado
    'P': 'Pts', 'J': 'Jogos', 'PPJ': 'PPJ', 'V': 'V', 'E': 'E', 'D': 'D',
    'GM': 'GM', 'GC': 'GC', 'SG': 'SG', 'GPJ': 'GPJ', 'AP': 'Aprv. (%)'
}

# 3. Cria o objeto Styler e aplica a formatação
styled_df = ranking_df_display[columns_to_display].rename(columns=column_names).style.format({
    'Pos | Time': lambda x: x, 
    'Aprv. (%)': "{:.1f}%",
    'PPJ': "{:.1f}",
    'GPJ': "{:.1f}"
})

# Remove o índice lateral (que não é mais necessário, pois a posição está na primeira coluna)
styled_df = styled_df.hide(axis='index') 

# 4. Converte e renderiza como HTML
html_table = styled_df.to_html(escape=False) 
st.markdown(html_table, unsafe_allow_html=True) 

st.markdown("---")
# # NOTA: O Streamlit renderiza HTML em DataFrames via .style.format() e .apply()
# # desde que o HTML seja bem formado. A chave 'Time' (que é 'Time_HTML') deve ser formatada como string.
# st.dataframe(styled_df, use_container_width=True) 

# st.markdown("---")

# --- Legenda (Ajudar o usuário a entender as colunas)
st.markdown("""
### Legenda das Colunas
* **Pos:** Posição no Ranking (Ordenação atual).
* **Pts:** Total de Pontos.
* **Jogos:** Jogos Disputados (no filtro selecionado).
* **PPJ:** **Pontos por Jogo** ($\t{Pts} / \t{Jogos}$).
* **V, E, D:** Vitórias, Empates, Derrotas.
* **GM:** Gols Marcados.
* **GC:** Gols Sofridos.
* **SG:** Saldo de Gols ($\t{GM} - \t{GC}$).
* **GPJ:** **Gols por Jogo** ($\t{GM} / \t{Jogos}$).
* **Aprv. (%):** Aproveitamento em Pontos.
""")