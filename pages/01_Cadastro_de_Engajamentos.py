import streamlit as st
import sqlite3
import pandas as pd

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

# --- Cabeçalho ---
st.markdown("<h3>Registro de Engajamentos</h3>", unsafe_allow_html=True)

# --- Funções para gerenciar o banco de dados SQLite ---

def init_db():
    conn = sqlite3.connect("engajamentos.db")
    c = conn.cursor()
    # Cria a tabela se não existir (sem a coluna 'funcionando')
    c.execute('''
        CREATE TABLE IF NOT EXISTS engajamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            engajamento_id TEXT NOT NULL
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

def update_funcionamento(row_id, funcionando):
    conn = sqlite3.connect("engajamentos.db")
    c = conn.cursor()
    c.execute("UPDATE engajamentos SET funcionando = ? WHERE id = ?", (funcionando, row_id))
    conn.commit()
    conn.close()

# Inicializa o banco e adiciona a coluna se necessário
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

# --- Exibe os engajamentos cadastrados ---
st.markdown("### Engajamentos Salvos")
rows = get_engajamentos()
if rows:
    df = pd.DataFrame(rows, columns=["id", "Nome", "ID do Engajamento", "Funcionando?"])
    st.table(df)
else:
    st.info("Nenhum engajamento cadastrado ainda.")

# --- Botões para atualizar o status de funcionamento ---
st.markdown("### Atualizar Status de Funcionamento")
if rows:
    for row in rows:
        col1, col2 = st.columns([3,1])
        with col1:
            st.write(f"**Nome:** {row[1]} | **ID:** {row[2]} | **Funcionando?:** {row[3]}")
        with col2:
            if row[3] == "Sim":
                if st.button("Marcar como Não Funcionando", key=f"btn_{row[0]}"):
                    update_funcionamento(row[0], "Não")
                    st.success(f"Engajamento '{row[1]}' atualizado para Não Funcionando.")
                    st.experimental_rerun()
            else:
                st.write("Já marcado como Não")
