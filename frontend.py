import streamlit as st
import httpx

# Configuração da Página
st.set_page_config(
    page_title="Strands AI Agent",
    page_icon="🤖",
    layout="centered"
)

# Estilização Customizada
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Título e Descrição
st.title("🤖 Strands AI Agent")
st.markdown("Interaja com o Agente Inteligente capaz de conversar e realizar cálculos matemáticos.")

# Configuração da URL da API
with st.sidebar:
    st.header("⚙️ Configurações")
    api_url = st.text_input("URL da API", "http://127.0.0.1:8000/chat")
    st.info("Certifique-se de que o Backend (Uvicorn) está rodando.")

    if st.button("Verificar Saúde da API"):
        try:
            # Tenta bater no endpoint de health
            health_url = api_url.replace("/chat", "/health")
            res = httpx.get(health_url, timeout=2.0)
            if res.status_code == 200:
                st.success("API Online! 🟢")
            else:
                st.warning(f"Status Inesperado: {res.status_code} 🟡")
        except:
            st.error("API Offline ou Inacessível 🔴")

# Inicialização do Histórico de Chat na Sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Renderizar mensagens antigas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do Usuário
if prompt := st.chat_input("Digite sua mensagem aqui..."):
    # mensagem do usuário ao histórico visual
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # spinner enquanto a IA pensa
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")

        try:
            # Chamada para a API FastAPI
            response = httpx.post(
                api_url,
                json={"message": prompt},
                timeout=30.0
            )

            if response.status_code == 200:
                ai_response = response.json().get("response", "Erro: Resposta vazia.")
                message_placeholder.markdown(ai_response)
                # Salva resposta no histórico
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            else:
                error_msg = f"Erro na API: {response.status_code} - {response.text}"
                message_placeholder.error(error_msg)

        except httpx.ConnectError:
            message_placeholder.error("Erro de Conexão: O servidor FastAPI está desligado?")
        except Exception as e:
            message_placeholder.error(f"Erro inesperado: {str(e)}")