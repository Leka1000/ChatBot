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

# Estilização customizada com st.markdown para bordas e visual profissional
st.markdown(
    """
    <style>
    /* Estilização geral do container principal */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
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
# 2. CONFIGURAÇÃO DA API (MICROSOFT FOUNDRY)
# ==========================================
API_KEY = "6t2pTNsmNafDyo53MDAFIrvvQRBZXP7dLcr5j3TLxMS34LQVq3ZUJQQJ99CHACHYHv6XJ3w3AAAAACOGT7os"
DEPLOYMENT_NAME = "gpt-4.1-mini"
ENDPOINT = "https://marcelomaffeis-05082026-resource.services.ai.azure.com/"

# Inicialização do cliente Azure OpenAI compatível com o SDK oficial da OpenAI
try:
  client = AzureOpenAI(
      api_key=API_KEY,
      api_version="2024-08-01-preview",
      azure_endpoint=ENDPOINT,
  )
except Exception as e:
  st.error(f"Erro ao inicializar o cliente Azure OpenAI: {e}")

# ==========================================
# 3. BARRA LATERAL E SISTEMA RAG
# ==========================================
st.sidebar.title("⚙️ Configurações & RAG")
st.sidebar.markdown(
    "Envie um documento de referência para contextualizar as respostas do bot."
)

uploaded_file = st.sidebar.file_uploader(
    "Escolha um arquivo (PDF ou TXT)", type=["pdf", "txt"]
)


def extrair_texto_arquivo(arquivo):
  """Extrai o texto de arquivos PDF ou TXT carregados na interface."""
  texto = ""
  if arquivo is not None:
    try:
      if arquivo.type == "application/pdf":
        leitor_pdf = PdfReader(arquivo)
        for pagina in leitor_pdf.pages:
          texto_pagina = pagina.extract_text()
          if texto_pagina:
            texto += texto_pagina + "\n"
      elif arquivo.type == "text/plain":
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
        f"Arquivo carregado com sucesso! ({len(contexto_rag)} caracteres"
        " extraídos)"
    )

# ==========================================
# 4. INTERFACE DE CHAT E LÓGICA DE ESTADO
# ==========================================
st.title("🤖 Assistente Inteligente com RAG")
st.markdown(
    "Faça perguntas gerais ou utilize o documento enviado na barra lateral para"
    " consultas contextuais."
)

# Inicializa o histórico de mensagens no session_state
if "messages" not in st.session_state:
  st.session_state.messages = []

# Exibe o histórico de mensagens anteriores
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Captura a entrada do usuário
if prompt_usuario := st.chat_input("Digite sua mensagem aqui..."):
  # Adiciona a mensagem do usuário ao histórico
  st.session_state.messages.append(
      {"role": "user", "content": prompt_usuario}
  )
  with st.chat_message("user"):
    st.markdown(prompt_usuario)

  # Constrói o prompt do sistema integrando o RAG básico (se houver documento)
  sistema_prompt = (
      "Você é um assistente virtual prestativo e profissional especializado em"
      " responder dúvidas com base no contexto fornecido."
  )
  if contexto_rag:
    sistema_prompt += (
        "\n\nUtilize obrigatoriamente as informações do documento abaixo para"
        " embasar suas respostas, caso sejam relevantes para a pergunta do"
        " usuário:\n--- INÍCIO DO DOCUMENTO ---\n"
        f"{contexto_rag}\n--- FIM DO DOCUMENTO ---"
    )

  # Monta o payload de mensagens para a API
  mensagens_api = [{"role": "system", "content": sistema_prompt}]
  # Adiciona o histórico recente para manter o contexto da conversa
  for msg in st.session_state.messages:
    mensagens_api.append({"role": msg["role"], "content": msg["content"]})

  # Gera a resposta do modelo na interface
  with st.chat_message("assistant"):
    with st.spinner("Pensando..."):
      try:
        resposta = client.chat.completions.create(
            model=DEPLOYMENT_NAME, messages=mensagens_api, temperature=0.7
        )
        resposta_texto = resposta.choices[0].message.content
        st.markdown(resposta_texto)

        # Salva a resposta no histórico do session_state
        st.session_state.messages.append(
            {"role": "assistant", "content": resposta_texto}
        )
      except Exception as e:
        erro_msg = f"Ocorreu um erro ao comunicar com a API do Microsoft Foundry: {e}"
        st.error(erro_msg)
