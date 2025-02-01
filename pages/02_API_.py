import streamlit as st
import requests
import json

# Injeção de CSS customizado
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

# Cabeçalho e mensagem informativa
st.markdown("<h3>🔒 Área restrita a desenvolvedores</h3>", unsafe_allow_html=True)

# Inicializa o estado de login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Se o usuário não estiver autenticado, exibe o formulário de login
if not st.session_state.logged_in:
    with st.form("login_form"):
        senha = st.text_input("Digite a senha para acessar a área de desenvolvedor", type="password")
        submitted = st.form_submit_button("Entrar")
        if submitted:
            # Defina a senha correta aqui
            if senha == "timeiagc":
                st.session_state.logged_in = True
                st.success("Acesso autorizado!")
            else:
                st.error("Senha incorreta. Tente novamente.")
    # Se ainda não autenticado, interrompe a execução para não exibir o restante da página
    st.stop()

# --- A partir daqui, o usuário está autenticado e o conteúdo da API é exibido ---

# Configurações da API
API_KEY = "9A*fw(I0@tni*lW(LUX(K"  # Substitua pela sua chave de API
API_URL = "https://www.smmraja.com/api/v3"

def criar_pedidos_em_lote(api_key, api_url, service_ids_str, links_str, quantidade):
    # Processa os IDs (espera exatamente 3 separados por vírgula)
    service_ids = [sid.strip() for sid in service_ids_str.split(",") if sid.strip()]
    if len(service_ids) != 3:
        return "Erro: Insira exatamente 3 IDs de serviço separados por vírgula."
    
    # Processa os links (um por linha)
    links = [link.strip() for link in links_str.splitlines() if link.strip()]
    if not links:
        return "Erro: Nenhum link foi inserido."
    
    if not quantidade.isdigit():
        return "Erro: A quantidade deve ser um número válido."
    
    quantidade = int(quantidade)
    resultados = []
    
    for service_id in service_ids:
        for link in links:
            payload = {
                "key": api_key,
                "action": "add",
                "service": service_id,
                "link": link,
                "quantity": quantidade
            }
            try:
                response = requests.post(api_url, data=payload)
                response_data = response.json()
                resultados.append({
                    "ID": service_id,
                    "Link": link,
                    "Resposta": response_data
                })
            except json.JSONDecodeError:
                resultados.append({
                    "ID": service_id,
                    "Link": link,
                    "Erro": f"Resposta inválida: {response.text}"
                })
            except Exception as e:
                resultados.append({
                    "ID": service_id,
                    "Link": link,
                    "Erro": str(e)
                })
    
    # Formata os resultados para exibição
    resultado_texto = "\n\n".join([
        f"**ID:** {res['ID']} | **Link:** {res['Link']}\n" +
        (f"**Resposta:** {json.dumps(res['Resposta'], indent=2)}" if "Resposta" in res 
         else f"**Erro:** {res['Erro']}")
        for res in resultados
    ])
    return resultado_texto

# Interface para envio dos dados à API
service_ids = st.text_input(
    "📄 IDs do Serviço (separados por vírgula)",
    placeholder="Ex: 12345,67890,54321"
)
links = st.text_area(
    "🔗 Links",
    placeholder="Cole seus links aqui (um por linha)"
)
quantidade = st.text_input(
    "🔢 Quantidade",
    placeholder="Ex: 100"
)

if st.button("📤 Enviar Pedidos"):
    resultado = criar_pedidos_em_lote(API_KEY, API_URL, service_ids, links, quantidade)
    st.markdown("### 📈 Resultados")
    st.text_area("", resultado, height=300)
