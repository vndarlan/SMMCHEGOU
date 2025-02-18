# Home.py
import streamlit as st

st.set_page_config(
    page_title="SMMCHEGOU",  # Título que aparecerá na aba do navegador
    page_icon=":heart:",              # Opcional: ícone (pode ser um emoji ou caminho para um arquivo)
    layout="centered"                     # Opcional: define o layout da página
)

# Injetando o CSS customizado para manter a identidade visual
custom_css = """
<style>
:root {
    --primary-color: #1A1A2E;
    --secondary-color: rgb(255, 0, 212);
    --accent-color: rgb(63, 63, 70);
    --button-color: rgb(33, 150, 223);
    --button-hover: rgb(10, 9, 110);
    --text-color: #FFFFFF;
}
body {
    background-color: var(--primary-color);
    color: var(--text-color);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1, h2, h3, h4, h5, h6 {
    color: var(--accent-color);
    text-align: center;
    margin-bottom: 20px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Conteúdo da página de layout
st.markdown("<h1>SMMCHEGOU</h1>", unsafe_allow_html=True)
st.markdown(
    """
    - Compre engajmento em poucos cliques 
    - Acessar a página de **API de Engajamento** para enviar pedidos à plataforma.
    
    Utilize o menu lateral para acessar a página de API.
    """
)
