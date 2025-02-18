import streamlit as st
import sqlite3
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

st.set_page_config(
    page_title="SMMCHEGOU",  # Título que aparecerá na aba do navegador
    page_icon=":heart:",              # Opcional: ícone (pode ser um emoji ou caminho para um arquivo)
    layout="wide"                     # Opcional: define o layout da página
)

# --- Injeção de CSS customizado ---
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
div.stButton > button {
    background-color: var(--button-color);
    color: var(--text-color);
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-size: 16px;
    transition: background 0.3s ease;
}
div.stButton > button:hover {
    background-color: var(--button-hover);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("<h3>Registro de Engajamentos</h3>", unsafe_allow_html=True)

# --- Funções para gerenciar o banco de dados SQLite ---
def init_db():
    conn = sqlite3.connect("engajamentos.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS engajamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            engajamento_id TEXT NOT NULL,
            funcionando TEXT NOT NULL DEFAULT 'Sim'
        )
    ''')
    conn.commit()
    conn.close()

def add_funcionando_column():
    conn = sqlite3.connect("engajamentos.db")
    c = conn.cursor()
    c.execute("PRAGMA table_info(engajamentos)")
    columns = [col[1] for col in c.fetchall()]
    if "funcionando" not in columns:
        c.execute("ALTER TABLE engajamentos ADD COLUMN funcionando TEXT NOT NULL DEFAULT 'Sim'")
        conn.commit()
    conn.close()

def insert_engajamento(nome, engajamento_id):
    conn = sqlite3.connect("engajamentos.db")
    c = conn.cursor()
    c.execute("INSERT INTO engajamentos (nome, engajamento_id, funcionando) VALUES (?, ?, ?)", 
              (nome, engajamento_id, "Sim"))
    conn.commit()
    conn.close()

def get_engajamentos():
    conn = sqlite3.connect("engajamentos.db")
    c = conn.cursor()
    c.execute("SELECT id, nome, engajamento_id, funcionando FROM engajamentos")
    rows = c.fetchall()
    conn.close()
    return rows

def update_engajamento(row_id, nome, engajamento_id, funcionando):
    conn = sqlite3.connect("engajamentos.db")
    c = conn.cursor()
    c.execute("UPDATE engajamentos SET nome=?, engajamento_id=?, funcionando=? WHERE id=?", 
              (nome, engajamento_id, funcionando, row_id))
    conn.commit()
    conn.close()

# Inicializa o banco de dados e garante que a coluna 'funcionando' exista
init_db()
add_funcionando_column()

# --- Formulário para cadastro de engajamentos ---
with st.form("cadastro_engajamento"):
    engajamento_nome = st.text_input("Nome do Engajamento", placeholder="Digite o nome do engajamento")
    engajamento_id = st.text_input("ID do Engajamento", placeholder="Digite o ID do engajamento")
    submitted = st.form_submit_button("Salvar Engajamento")
    if submitted:
        if engajamento_nome and engajamento_id:
            insert_engajamento(engajamento_nome, engajamento_id)
            st.success("Engajamento salvo com sucesso!")
        else:
            st.error("Por favor, preencha ambos os campos.")

# --- Exibe os engajamentos cadastrados em uma tabela editável usando AgGrid ---
st.markdown("### Engajamentos Cadastrados (Tabela Editável)")
rows = get_engajamentos()
if rows:
    df = pd.DataFrame(rows, columns=["ID", "Nome", "ID do Engajamento", "Funcionando?"])
    
    # Configura o AgGrid
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_default_column(editable=True)
    # Torna a coluna "ID" somente leitura
    gb.configure_column("ID", editable=False)
    gridOptions = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=True,
    )
    edited_df = grid_response['data']

    if st.button("Salvar alterações"):
        for _, row in edited_df.iterrows():
            update_engajamento(row["ID"], row["Nome"], row["ID do Engajamento"], row["Funcionando?"])
        st.success("Atualizações salvas com sucesso!")
        st.experimental_rerun()
else:
    st.info("Nenhum engajamento cadastrado ainda.")
