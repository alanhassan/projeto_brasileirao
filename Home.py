import streamlit as st

# --- Configuração da Página ---
st.set_page_config(
    page_title="Início - Dashboard CBF",
    layout="wide"
)

# --- CSS Customizado ---
page_bg_img = """
<style>
/* 1. Imagem de fundo */
[data-testid="stAppViewContainer"] {
    background-image: url("https://img.freepik.com/vetores-gratis/fundo-abstrato-realista-de-futebol_52683-67579.jpg?semt=ais_hybrid&w=740&q=80");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* 2. Fundo transparente para o container principal */
[data-testid="stHeader"], [data-testid="stMainBlockContainer"] {
    background-color: rgba(0, 0, 0, 0);
}

/* --- 3. CONTROLE DE FONTES --- */

/* Título Principal (st.title) */
h1 {
    font-size: 3rem !important;
    font-weight: 800 !important;
}

/* Cabeçalhos (st.header) */
h2 {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
}

/* Textos padrões, parágrafos e listas (st.markdown) */
[data-testid="stMarkdownContainer"] p, li {
    font-size: 1.2rem !important;
    line-height: 1.6 !important;
}

/* Texto dentro do st.info ou outros alerts */
.stAlert p {
    font-size: 1.1rem !important;
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
* **⚽ Visão Time:** Evolução, pontuação e retrospecto por equipe.
* **🏆 Visão Ranking:** Tabela de classificação e desempenho (Casa/Fora).
* **⚔️ Duelo Times:** Comparativo e resultados do confronto direto. 
""")

# --- Rodapé ---
st.markdown("<br><hr><p style='text-align: center; color: #1E1E1E; font-weight: bold; font-size: 1.1rem;'>Dashboard de Análise de Performance | Autoria de Alan W. Hassan</p>", unsafe_allow_html=True)