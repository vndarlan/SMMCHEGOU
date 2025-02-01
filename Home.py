import streamlit as st

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
st.markdown("<h1>Bem-vindo à Aplicação de Engajamento GC</h1>", unsafe_allow_html=True)
st.markdown(
    """
    ### Sobre a Aplicação

    Nesta aplicação você poderá:
    - Visualizar informações de layout e instruções gerais.
    - Acessar a página de **API de Engajamento** para enviar pedidos à plataforma.
    
    Utilize o menu lateral (ou a navegação do Streamlit) para acessar a página de API.
    """
)
