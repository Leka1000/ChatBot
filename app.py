import io
import os
from openai import AzureOpenAI
from pypdf import PdfReader
import streamlit as st

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILO (CSS)
# ==========================================
st.set_page_config(
    page_title="ChatBot RAG - Microsoft Foundry",
    page_icon="🤖",
    layout="centered",
)

st.markdown(
    """
    <style>
    /* Estilização geral do container principal */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
    }
    
    /* Borda estilizada ao redor da área de chat/aplicação */
    .chat-container {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Personalização da barra lateral */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e0e0e0;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. BARRA LATERAL - CONFIGURAÇÕES & RAG
# ==========================================
st.sidebar.title("⚙️ Configurações & RAG")
st.sidebar.markdown(
    "Insira suas credenciais do Microsoft Foundry com segurança para estabelecer a conexão."
)

minha_chave = st.sidebar.text_input("minha_chave (API Key)", type="password")
meu_endpoint = st.sidebar.text_input(
    "meu_endpoint", 
    placeholder="https://seu-recurso.services.ai.azure.com/"
)
meu_modelo = st.sidebar.text_input(
    "meu_modelo", 
    value="gpt-4.1-mini"
)

st.sidebar.markdown("---")
st.sidebar.markdown("Envie um documento de referência para contextualizar as respostas do bot.")

uploaded_file = st.sidebar.file_uploader(
    "Escolha um arquivo (PDF ou TXT)", type=["pdf", "txt"]
)


def extrair_texto_arquivo(arquivo):
    """Extrai o texto de arquivos PDF ou TXT carregados na interface."""
    texto = ""
    if arquivo is not None:
        try:
            nome_arquivo = arquivo.name.lower()
            if nome_arquivo.endswith(".pdf"):
                leitor_pdf = PdfReader(arquivo)
                for pagina in leitor_pdf.pages:
                    texto_pagina = pagina.extract_text()
                    if texto_pagina:
                        texto += texto_pagina + "\n"
            elif nome_arquivo.endswith(".txt"):
                texto = arquivo.getvalue().decode("utf-8")
        except Exception as e:
            st.sidebar.error(f"Erro ao processar o arquivo: {e}")
    return texto


# Processa o arquivo se houver upload
contexto_rag = ""
if uploaded_file is not None:
    with st.sidebar.status("Processando documento...", expanded=False):
        contexto_rag = extrair_texto_arquivo(uploaded_file)
        st.sidebar.success(
            f"Arquivo carregado com sucesso! ({len(contexto_rag)} caracteres extraídos)"
        )

# ==========================================
# 3. INICIALIZAÇÃO DO CLIENTE AZURE OPENAI
# ==========================================
client = None
if minha_chave and meu_endpoint and meu_modelo:
    try:
        client = AzureOpenAI(
            api_key=minha_chave,
            api_version="2024-08-01-preview",
            azure_endpoint=meu_endpoint,
        )
    except Exception as e:
        st.error(f"Erro ao inicializar o cliente Azure OpenAI: {e}")

# ==========================================
# 4. INTERFACE DE CHAT E LÓGICA DE ESTADO
# ==========================================
st.title("🤖 Assistente Inteligente com RAG")
st.markdown(
    "Faça perguntas gerais ou utilize o documento enviado na barra lateral para "
    "consultas contextuais."
)

if not minha_chave or not meu_endpoint or not meu_modelo:
    st.warning("⚠️ Por favor, preencha **minha_chave**, **meu_endpoint** e **meu_modelo** na barra lateral para iniciar o chat.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt_usuario := st.chat_input("Digite sua mensagem aqui..."):
    if not client:
        st.error("Conexão não estabelecida. Verifique se preencheu todas as credenciais na barra lateral.")
    else:
        st.session_state.messages.append(
            {"role": "user", "content": prompt_usuario}
        )
        with st.chat_message("user"):
            st.markdown(prompt_usuario)

        sistema_prompt = (
            "Você é um assistente virtual prestativo e profissional especializado em "
            "responder dúvidas com base no contexto fornecido."
        )
        if contexto_rag:
