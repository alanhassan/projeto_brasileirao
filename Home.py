import streamlit as st

# --- Configuração da Página ---
st.set_page_config(
    page_title="Início - Dashboard CBF",
    layout="wide"
)

# --- CSS para Fundo Transparente (Glassmorphism) ---
page_bg_img = """
<style>
/* 1. Imagem de fundo no app */
[data-testid="stAppViewContainer"] {
    background-image: url("https://img.freepik.com/vetores-gratis/fundo-abstrato-realista-de-futebol_52683-67579.jpg?semt=ais_hybrid&w=740&q=80");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* 2. Remove cores de fundo padrão */
[data-testid="stHeader"], [data-testid="stMainBlockContainer"] {
    background-color: rgba(0, 0, 0, 0);
}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# --- Conteúdo da Página ---
st.title("⚽ Dashboard de Análise do Campeonato")
st.markdown("---")

st.header("Seja Bem-vindo!")
st.info("Utilize o menu de navegação na **barra lateral** à esquerda para acessar as diferentes seções de análise do campeonato.", icon="⬅️")

st.markdown("""
## 📋 Páginas Disponíveis
* **⚽ Visão Time:** Análise detalhada por time, incluindo evolução de posição, pontos, e sequências de resultados.
* **🏆 Visão Ranking:** Classificação atual dos times, com indicadores de performance e filtros de local de jogo (casa/ fora).
* **⚔️ Duelo Times:** Indicadores dos times selecionados e resultados do 1º e 2º Turno entre os mesmos. 
""")

# --- Rodapé ---
st.markdown("<br><hr><p style='text-align: center; color: #1E1E1E; font-weight: bold;'>Dashboard de Análise de Performance | Autoria de Alan W. Hassan</p>", unsafe_allow_html=True)