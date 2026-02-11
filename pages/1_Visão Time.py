import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import os # Importação adicionada para verificar o caminho

# --- Configurações Iniciais ---
st.set_page_config(layout="wide", page_title="⚽ Performance dos Times - Análise Detalhada")

# --- Variáveis Globais e Funções de Estilo/Visualização ---
# Dicionário de Logos dos Times
TEAM_LOGOS = {
    'Fortaleza Ec Saf': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Fortaleza_Esporte_Clube_logo.png/640px-Fortaleza_Esporte_Clube_logo.png',
    'Juventude': 'https://upload.wikimedia.org/wikipedia/de/c/cd/Juventude_logo.svg',
    'Cruzeiro Saf': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Cruzeiro_Esporte_Clube_%28logo%29.svg/250px-Cruzeiro_Esporte_Clube_%28logo%29.svg.png',
    'Vasco da Gama S.a.f.': 'https://upload.wikimedia.org/wikipedia/pt/thumb/8/8b/EscudoDoVascoDaGama.svg/950px-EscudoDoVascoDaGama.svg.png',
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
    'Atlético Mineiro Saf': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Atletico_mineiro_galo.png/250px-Atletico_mineiro_galo.png',
    'Santos Fc': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Santos_logo.svg/1045px-Santos_logo.svg.png',
    'Fluminense': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Fluminense_Football_Club.svg/250px-Fluminense_Football_Club.svg.png',
    'Vitória': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Esporte_Clube_Vit%C3%B3ria.png/640px-Esporte_Clube_Vit%C3%B3ria.png',
    'Chapecoense': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/S%C3%ADmbolo_Chapecoense_sem_estrelas.svg/640px-S%C3%ADmbolo_Chapecoense_sem_estrelas.svg.png',
    'Athletico Paranaense': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Athletico_Paranaense_%28Logo_2019%29.svg/640px-Athletico_Paranaense_%28Logo_2019%29.svg.png',
    'Vasco da Gama Saf': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Escudo_Vasco_1920.png/640px-Escudo_Vasco_1920.png',
    'Coritiba S.a.f.': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Coritiba_Foot_Ball_Club_logo.svg/640px-Coritiba_Foot_Ball_Club_logo.svg.png',
    'Remo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Clube_do_Remo.svg/640px-Clube_do_Remo.svg.png',
}
consistent_blue = '#1f77b4' # Tom de azul consistente para os gráficos
# Mantenha o caminho original, mas adicione uma nota de aviso
FILE_PATH = 'df_final.xlsx' 

def format_metric_value_inline(total, detail_c, detail_f, color='gray', emoji=''):
    """Retorna o HTML formatado para o valor total e o detalhe C/F ao lado, mais limpo."""
    # 1. HTML para o detalhe (menor e colorido)
    detail_html = f'<span style="font-size: 14px; color: {color}; font-weight: bold; margin-left: 10px;">({detail_c} C / {detail_f} F)</span>'
    # 2. Combina o total, emoji e o HTML do detalhe
    return f'<div style="display: flex; align-items: center;"><span style="font-size: 32px; font-weight: bold;">{emoji} {total}</span>{detail_html}</div>'

# --- Funções de Gráficos (Modularidade) ---

def create_position_chart(df_team, all_teams_size, consistent_blue):
    """Cria o gráfico de evolução da posição no ranking."""
    if df_team.empty:
        # Retorna um objeto Altair vazio ou um st.warning (que Streamlit lida automaticamente)
        return st.warning("Dados insuficientes para o gráfico de Posição.")

    min_posicao = df_team['Posicao_Jogo'].min()
    max_posicao = df_team['Posicao_Jogo'].max()

    df_team['Destaque_Posicao'] = np.where(
        df_team['Posicao_Jogo'] == min_posicao, 'Melhor Posição',
        np.where(df_team['Posicao_Jogo'] == max_posicao, 'Pior Posição', 'Normal')
    )

    chart_base = alt.Chart(df_team).encode(
        x=alt.X('Ordem_Jogo', title='Rodada'),
        y=alt.Y('Posicao_Jogo', title='Posição no Ranking', scale=alt.Scale(domain=[1, all_teams_size], reverse=True)),
        tooltip=['Ordem_Jogo', 'Posicao_Jogo', 'Time1', 'Adversario', 'Resultado']
    )

    chart_line = chart_base.mark_line(color=consistent_blue, point=True).interactive()

    chart_highlight = chart_base.mark_circle(size=100, opacity=1).encode(
        color=alt.Color('Destaque_Posicao',
                        scale=alt.Scale(domain=['Melhor Posição', 'Pior Posição', 'Normal'],
                                         range=['#198754', '#dc3545', 'transparent']), # Uso de cores mais vivas e transparent
                        legend=alt.Legend(title="Performance", orient='bottom')),
        strokeWidth=alt.value(2)
    ).transform_filter(
        alt.FieldOneOfPredicate(field='Destaque_Posicao', oneOf=['Melhor Posição', 'Pior Posição'])
    )

    return (chart_line + chart_highlight).properties(title="Evolução da Posição no Ranking").interactive()

def create_points_chart(df_team, consistent_blue):
    """Cria o gráfico de evolução de pontos acumulados."""
    if df_team.empty:
        return st.warning("Dados insuficientes para o gráfico de Pontos Acumulados.")

    return alt.Chart(df_team).mark_line(point=True, color=consistent_blue).encode(
        x=alt.X('Ordem_Jogo', title='Rodada'),
        y=alt.Y('Pontos_Acumulados_Calc', title='Pontos Acumulados'),
        tooltip=['Ordem_Jogo', 'Pontos_Acumulados_Calc', 'Adversario', 'Resultado']
    ).properties(title="Evolução dos Pontos Acumulados").interactive()


def create_goal_difference_chart(df_team, consistent_blue):
    """Cria o gráfico de evolução do Saldo de Gols Acumulado com área colorida e linha de conexão contínua."""
    if df_team.empty:
        return st.warning("Dados insuficientes para o gráfico de Saldo de Gols.")

    # 1. Calculando Saldo de Gols Acumulado e a Performance
    df_team['Saldo_Gols_Acumulado'] = df_team['Saldo_Jogo'].cumsum()
    # Mantemos esta coluna para a coloração da ÁREA e PONTOS
    df_team['Performance_Saldo'] = df_team['Saldo_Gols_Acumulado'].apply(lambda x: 'Positivo' if x >= 0 else 'Negativo')

    color_positivo = '#198754' # Verde
    color_negativo = '#dc3545' # Vermelho
    color_scale = alt.Scale(domain=['Positivo', 'Negativo'], range=[color_positivo, color_negativo])
    
    chart_base = alt.Chart(df_team).encode(
        x=alt.X('Ordem_Jogo', title='Rodada'),
        y=alt.Y('Saldo_Gols_Acumulado', title='Saldo de Gols Acumulado', scale=alt.Scale(zero=False)),
        tooltip=['Ordem_Jogo', 'Saldo_Gols_Acumulado', 'Adversario']
    )
    
    # --- 1. Linha Zero de Referência ---
    rule = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='gray', strokeDash=[3, 3]).encode(y='y')
    
    # --- 2. ÁREA: ÚNICA, COLORIDA CONDICIONALMENTE ---
    chart_area = chart_base.mark_area(opacity=0.3, line=False).encode(
        y2=alt.value(0), # Define a base da área em y=0
        # A cor do PREENCHIMENTO é CONDICIONAL
        color=alt.Color('Performance_Saldo:N', scale=color_scale, legend=None) 
    )
    
    # --- 3. LINHA DE CONEXÃO CONTÍNUA (Preta ou Azul Consistente) ---
    chart_continuous_line = chart_base.mark_line(
        color='gray' # Linha cinza, como solicitado, para garantir a continuidade
    ).encode() 
    
    # --- 4. Pontos Coloridos (Manter a cor condicional nos pontos) ---
    chart_points_colored = chart_base.mark_circle(size=60).encode(
        color=alt.Color('Performance_Saldo:N', 
                        scale=color_scale,
                        legend=alt.Legend(title='Saldo Acumulado', orient='bottom'))
    )

    # Combina a Linha Zero, a Área Colorida, a Linha Contínua e os Pontos
    final_chart = (rule + chart_area + chart_continuous_line + chart_points_colored).properties(title="Evolução do Saldo de Gols").interactive()
    
    return final_chart

@st.cache_data
def load_data(file_path):
    """Carrega os dados do CSV. Adiciona aviso sobre o caminho local."""
    if not os.path.exists(file_path):
          st.error(f"Erro: O arquivo não foi encontrado no caminho especificado: `{file_path}`. Por favor, verifique o caminho.")
          # Retorna um DataFrame vazio para evitar que o resto do código quebre.
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


def calculate_game_metrics(df_team, team_name):
    """Calcula o Saldo de Gols e Pontos por Jogo para o time selecionado."""
    # 1. Determinar Gols Marcados (GS), Gols Sofridos (GC) e Adversário (Opponent)
    df_team['GS'] = df_team.apply(
        lambda row: row['Gols1'] if row['Time1'] == team_name else row['Gols2'], axis=1
    )
    df_team['GC'] = df_team.apply(
        lambda row: row['Gols2'] if row['Time1'] == team_name else row['Gols1'], axis=1
    )

    df_team['Saldo_Jogo'] = df_team['GS'] - df_team['GC']
    df_team['Adversario'] = df_team.apply(
        lambda row: row['Time2'] if row['Time1'] == team_name else row['Time1'], axis=1
    )

    # 2. Calcular Pontos por Jogo e Pontos Acumulados do zero
    df_team['Pontos_Jogo'] = df_team['Resultado'].map({'V': 3, 'E': 1, 'D': 0})
    df_team['Pontos_Acumulados_Calc'] = df_team['Pontos_Jogo'].cumsum()

    return df_team

# NOVO: Função para encontrar o início e fim da maior sequência
def get_max_streak_rounds(df_team, target_result, no_target_result=False):
    """
    Encontra o tamanho, rodada inicial e final da maior sequência de um resultado.
    """
    if df_team.empty:
        return 0, None, None

    # Define a condição booleana
    if no_target_result:
        # Sequência sem vencer: !V (Empate ou Derrota)
        condition = df_team['Resultado'].ne(target_result) 
    else:
        # Sequência de Vitória/Empate/Derrota: == target_result
        condition = df_team['Resultado'].eq(target_result) 

    # 1. Cria um ID de grupo para cada sequência
    group_id = condition.ne(condition.shift()).cumsum()
    
    # Filtra apenas os grupos onde a condição é True
    streaks = df_team[condition].copy()
    
    if streaks.empty:
        return 0, None, None

    # Atribui o ID do grupo apenas para os resultados que satisfazem a condição
    streaks['group'] = group_id
    
    # 2. Calcula o tamanho de cada grupo e identifica o(s) maior(es)
    streak_summary = streaks.groupby('group')['Ordem_Jogo'].agg(
        size='count',
        start_round='min',
        end_round='max'
    ).reset_index()

    if streak_summary.empty:
        return 0, None, None

    # Encontra a maior sequência
    max_streak_size = streak_summary['size'].max()
    
    # Filtra o registro da maior sequência (pode haver mais de uma com o mesmo tamanho)
    max_streak_row = streak_summary[streak_summary['size'] == max_streak_size].iloc[0]

    return max_streak_size, int(max_streak_row['start_round']), int(max_streak_row['end_round'])


# --- Carregamento de Dados ---
df = load_data(FILE_PATH)

if df.empty:
    st.warning("Não foi possível carregar os dados. Verifique o caminho do arquivo e se o Excel está fechado.")
    st.stop()


# --- Título e Seleção do Time (Melhorados) ---
st.title("⚽ Análise de Performance dos Times")
st.markdown("---") # Linha mais limpa após o título

# Container para os Selectboxes
with st.container():
    col_sel_team, col_sel_year = st.columns([2, 1])
    
    with col_sel_team:
        all_teams = pd.unique(df[['Time1', 'Time2']].values.ravel('K'))
        all_teams.sort()
        selected_team = st.selectbox("Selecione o Time:", all_teams)

    with col_sel_year:
        # Extrai anos únicos da coluna 'Ano'
        all_years = sorted(df['ano'].unique().tolist(), reverse=True)
        selected_year = st.selectbox("Selecione o Ano:", all_years)


# # Container para o Selectbox para melhor alinhamento
# with st.container():
#     col_sel_title, col_sel = st.columns([1, 4])
#     with col_sel_title:
#         st.subheader("Time Selecionado:")
#     with col_sel:
#         selected_team = st.selectbox(
#             "Selecione o Time para Análise:",
#             all_teams,
#             index=0,
#             label_visibility="collapsed" # Esconde o label duplicado
#         )

# NOVO: Define o URL do logo
current_logo_url = TEAM_LOGOS.get(
    selected_team,
    "https://placehold.co/200x200/eeeeee/333333?text=Logo+N/A"
)

# --- Filtragem e Preparação dos Dados do Time ---
# Filtra os dados onde o time selecionado está na coluna Time1 (assumindo que o dataframe já está preparado para isso)
df_team = df[(df['Time1'] == selected_team) & (df['ano'] == selected_year)].copy() # Remove duplicatas se houver, garantindo que cada jogo apareça apenas uma vez para o time selecionado.
df_team.drop_duplicates(subset=['Ordem_Jogo'], keep='first', inplace=True) 
df_team.sort_values(by='Ordem_Jogo', inplace=True) # Garantir a ordem cronológica

if df_team.empty:
    st.warning(f"Não foram encontrados jogos para o time '{selected_team}'.")
    st.stop()
    
df_team = calculate_game_metrics(df_team, selected_team)


# Variáveis globais de jogos e pontos
total_games = len(df_team)
total_points = df_team['Pontos_Acumulados_Calc'].iloc[-1] if not df_team.empty else 0


# --- CÁLCULOS PRINCIPAIS ---
if total_games > 0:
    # 1. Big Numbers
    posicao_atual = df_team['Posicao_Jogo'].iloc[-1]

    # NOVOS CÁLCULOS DE POSIÇÃO
    melhor_posicao = df_team['Posicao_Jogo'].min()
    pior_posicao = df_team['Posicao_Jogo'].max()

    aproveitamento_total = (total_points / (total_games * 3)) * 100

    df_casa = df_team[df_team['Local'] == 'C']
    points_casa = df_casa['Pontos_Jogo'].sum()
    games_casa = len(df_casa)   
    aproveitamento_casa = (points_casa / (games_casa * 3)) * 100 if games_casa > 0 else 0

    df_fora = df_team[df_team['Local'] == 'F']
    points_fora = df_fora['Pontos_Jogo'].sum()
    games_fora = len(df_fora)
    aproveitamento_fora = (points_fora / (games_fora * 3)) * 100 if games_fora > 0 else 0

    # 2. Resumo de Jogos
    # Certifique-se de que todas as combinações de (Resultado, Local) estão presentes para evitar erros de KeyError
    summary = df_team.groupby(['Resultado', 'Local']).size().unstack(fill_value=0)
    
    # Mapeamento para garantir que as chaves 'V', 'E', 'D', 'C', 'F' existam no summary
    results_map = {'V': 0, 'E': 0, 'D': 0}
    local_map = {'C': results_map.copy(), 'F': results_map.copy()}
    
    # Preencher o mapa com os dados calculados
    for res in ['V', 'E', 'D']:
        for loc in ['C', 'F']:
            if loc in summary.columns and res in summary.index:
                local_map[loc][res] = summary.loc[res, loc]

    vitorias_c = local_map['C']['V']
    vitorias_f = local_map['F']['V']
    empates_c = local_map['C']['E']
    empates_f = local_map['F']['E']
    derrotas_c = local_map['C']['D']
    derrotas_f = local_map['F']['D']

    # 3. Destaques de Sequências (AGORA COM AS RODADAS!)
    max_v, start_v, end_v = get_max_streak_rounds(df_team, 'V', no_target_result=False)
    max_sv, start_sv, end_sv = get_max_streak_rounds(df_team, 'V', no_target_result=True)
    
# =========================================================================
# --- SEÇÃO PRINCIPAL: VISÃO GERAL (Logo e Big Numbers) ---
# =========================================================================

# Uso de um container para dar um visual de 'cartão'
with st.container(border=True):
    col_logo, col_spacer, col_content = st.columns([1.5, 0.5, 8])

    # --- Coluna do Logo ---
    with col_logo:
        st.markdown('<div style="display: flex; margin-top: 125px; flex-direction: column; align-items: center; justify-content: center; height: 100%;">', unsafe_allow_html=True)
        
        # 
        st.image(current_logo_url, width=200) 
        
        # O texto fica com text-align: center; para centralizar SOB o logo
        st.markdown(f"<h4 style='text-align: center; color: {consistent_blue}; margin-top: 5px; margin-bottom: 0px;'>{selected_team}</h4>", unsafe_allow_html=True)
        
        st.markdown(f"<p style='text-align: center; font-size: 18px; color: #888; margin-top: 5px;'>Total de Jogos: {total_games}</p>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


    # --- Coluna do Conteúdo: Big Numbers ---
    with col_content:

        st.subheader("Posição na Tabela")
        col_pos1, col_pos2, col_pos3, col_pos4 = st.columns(4)
        
        col_pos1.metric("⭐ Posição Atual", f"{posicao_atual}º", delta_color='off')
        col_pos2.metric("🔝 Melhor Posição", f"{melhor_posicao}º", delta_color='off') # Melhor é o menor número
        col_pos3.metric("🔻 Pior Posição", f"{pior_posicao}º", delta_color='off') # Pior é o maior número
        # Coluna extra para manter o alinhamento
        col_pos4.markdown("")
        
        st.markdown("---") # Separador entre Posição e Aproveitamento
        
        st.subheader("Aproveitamento")
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("📊 Aproveitamento Total", f"{aproveitamento_total:.1f}%")
        col2.metric("🏠 Aproveitamento Casa", f"{aproveitamento_casa:.1f}%")
        col3.metric("✈️ Aproveitamento Fora", f"{aproveitamento_fora:.1f}%")

        st.markdown("---")

        st.subheader("Resultados (Total | Casa / Fora)")

        # RESUMO DE JOGOS (Com métricas customizadas, Casa/Fora ao lado)
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)

        # Coluna 1: Pontos Acumulados (substituindo o Total de Jogos, mais impactante)
        with col_s1:
            st.markdown("💰 Pontos Acumulados")
            st.markdown(f'<div style="font-size: 32px; font-weight: bold; color: {consistent_blue};">{total_points}</div>', unsafe_allow_html=True)


        # Coluna 2: Vitórias
        with col_s2:
            st.markdown("✅ Vitórias")
            vitorias_total = vitorias_c + vitorias_f
            html_vitorias = format_metric_value_inline(vitorias_total, vitorias_c, vitorias_f, color='green', emoji='')
            st.markdown(html_vitorias, unsafe_allow_html=True)

        # Coluna 3: Empates
        with col_s3:
            st.markdown("🤝 Empates")
            empates_total = empates_c + empates_f
            html_empates = format_metric_value_inline(empates_total, empates_c, empates_f, color='#000000', emoji='')
            st.markdown(html_empates, unsafe_allow_html=True)

        # Coluna 4: Derrotas
        with col_s4:
            st.markdown("❌ Derrotas")
            derrotas_total = derrotas_c + derrotas_f
            html_derrotas = format_metric_value_inline(derrotas_total, derrotas_c, derrotas_f, color='red', emoji='')
            st.markdown(html_derrotas, unsafe_allow_html=True)

st.markdown("---") # Separador visual


# =========================================================================
# --- SEÇÃO DE EVOLUÇÃO (Gráficos: ESCONDIDA COM EXPANDER) ---
# =========================================================================
# Conteúdo agora dentro do st.expander
# ALTERAÇÃO: Usando Markdown nativo para negrito.
with st.expander('**📊 Gráficos de Evolução**', expanded=True):
    # st.markdown("Visualize o desempenho do time rodada a rodada.")

    # Gráfico 1: Posição no Ranking (Agora ocupa a largura total)
    st.subheader("📈 Posição a cada Rodada")
    chart_posicao = create_position_chart(df_team, all_teams.size, consistent_blue)
    if not isinstance(chart_posicao, st.delta_generator.DeltaGenerator):
        st.altair_chart(chart_posicao, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True) # Espaçamento entre os gráficos

    # Gráfico 2: Pontos Acumulados (Agora abaixo do de Posição, ocupando a largura total)
    st.subheader("💰 Pontos Acumulados")
    chart_pontos = create_points_chart(df_team, consistent_blue)
    if not isinstance(chart_pontos, st.delta_generator.DeltaGenerator):
        st.altair_chart(chart_pontos, use_container_width=True)


    # NOVO GRÁFICO: Saldo de Gols Acumulado
    st.subheader("🥅 Saldo de Gols Acumulado")
    chart_saldo = create_goal_difference_chart(df_team, consistent_blue)
    if not isinstance(chart_saldo, st.delta_generator.DeltaGenerator):
        st.altair_chart(chart_saldo, use_container_width=True)

st.markdown("---") # Separador visual

# =========================================================================
# --- SEÇÃO DE DESTAQUES E SEQUÊNCIAS (Tipografia Ajustada: ESCONDIDA COM EXPANDER) ---
# =========================================================================

# Conteúdo agora dentro do st.expander
# ALTERAÇÃO: Usando Markdown nativo para negrito.
with st.expander('**✨ Destaques de Performance e Sequências**', expanded=True):
    # st.header("✨ Destaques de Performance e Sequências")
    col_d1, col_d2, col_d3, col_d4 = st.columns(4)

    # 1. Melhor Vitória (Max Saldo_Jogo onde Resultado='V')
    melhor_vitoria = df_team[df_team['Resultado'] == 'V'].sort_values(by='Saldo_Jogo', ascending=False).iloc[0] if vitorias_c + vitorias_f > 0 else None

    # 2. Pior Derrota (Min Saldo_Jogo onde Resultado='D')
    pior_derrota = df_team[df_team['Resultado'] == 'D'].sort_values(by='Saldo_Jogo', ascending=True).iloc[0] if derrotas_c + derrotas_f > 0 else None

    # --- Customização da Tipografia ---
    # Título: Aumentar fonte para um h4 equivalente
    # Resultado da Métrica: Reduzir a fonte (mantendo o negrito)
    STYLE_TITLE = "font-size: 25px; font-weight: bold; margin-bottom: 0px;"
    STYLE_METRIC = "font-size: 20px; font-weight: bold; margin-top: 5px;"


    with col_d1:
        st.markdown(f"<p style='{STYLE_TITLE}'>🏆 Melhor Vitória</p>", unsafe_allow_html=True)
        if melhor_vitoria is not None:
            local_desc = "Casa" if melhor_vitoria['Local'] == 'C' else "Fora"
            st.markdown(f"<p style='{STYLE_METRIC}'>Saldo: <span style='color: green;'>+{melhor_vitoria['Saldo_Jogo']}</span></p>", unsafe_allow_html=True)
            st.caption(f"Rodada {melhor_vitoria['Ordem_Jogo']} - {melhor_vitoria['Adversario']} ({local_desc})")
            st.caption(f"Placar: {melhor_vitoria['GS']} x {melhor_vitoria['GC']}")
        else:
            st.info("Nenhuma vitória registrada.", icon="ⓘ")

    with col_d2:
        st.markdown(f"<p style='{STYLE_TITLE}'>📉 Pior Derrota</p>", unsafe_allow_html=True)
        if pior_derrota is not None:
            local_desc = "Casa" if pior_derrota['Local'] == 'C' else "Fora"
            # Usa cor vermelha para o saldo negativo
            st.markdown(f"<p style='{STYLE_METRIC}'>Saldo: <span style='color: red;'>{pior_derrota['Saldo_Jogo']}</span></p>", unsafe_allow_html=True)
            st.caption(f"Rodada {pior_derrota['Ordem_Jogo']} - {pior_derrota['Adversario']} ({local_desc})")
            st.caption(f"Placar: {pior_derrota['GS']} x {pior_derrota['GC']}")
        else:
            st.info("Nenhuma derrota registrada.", icon="ⓘ")

    with col_d3:
        st.markdown(f"<p style='{STYLE_TITLE}'>🥇 Maior Sequência de Vitórias</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='{STYLE_METRIC}'>{max_v} Jogos</p>", unsafe_allow_html=True)
        
        # NOVO CAPTION PARA VITÓRIAS
        if max_v > 0 and start_v is not None and end_v is not None:
            st.caption(f"Rodadas {start_v} - {end_v}")
        elif max_v > 0:
            st.caption("Rodadas não calculadas (Erro interno).")
        else:
            st.caption("Aguardando sequência.")


    with col_d4:
        st.markdown(f"<p style='{STYLE_TITLE}'>🛑 Maior Sequência Sem Vencer</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='{STYLE_METRIC}'>{max_sv} Jogos</p>", unsafe_allow_html=True)
        
        # NOVO CAPTION PARA SEM VENCER
        if max_sv > 0 and start_sv is not None and end_sv is not None:
            st.caption(f"Rodadas {start_sv} - {end_sv}")
        elif max_sv > 0:
            st.caption("Rodadas não calculadas (Erro interno).")
        else:
            st.caption("Aguardando sequência.")


# --- Rodapé ---
st.markdown("<br><hr><p style='text-align: center; color: gray;'>Dashboard de Análise de Performance | Autoria de Alan W. Hassan</p>", unsafe_allow_html=True)