import streamlit as st

st.set_page_config(
    page_title="Início - Dashboard CBF",
    layout="wide"
)

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