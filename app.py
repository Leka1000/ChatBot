"Atue como um Desenvolvedor Sênior em Python e Streamlit. Escreva o código completo e funcional de um aplicativo de ChatBot em um único arquivo app.py. O sistema deve conter os seguintes requisitos:
1. Interface e Estilo (Borda):
Crie a interface usando Streamlit.
Aplique um CSS customizado (usando st.markdown) para criar uma borda estilizada ao redor da área principal do chat ou da aplicação, dando um aspecto profissional e bem acabado.
2. Configuração da API (Microsoft Foundry):
insira os dados para vincular com a plataforma do Microsoft Foundry no próprio códígo:
API = "6t2pTNsmNafDyo53MDAFIrvvQRBZXP7dLcr5j3TLxMS34LQVq3ZUJQQJ99CHACHYHv6XJ3w3AAAAACOGT7os"
modelo = "gpt-4.1-mini" # Certifique-se de que este é o NOME DO DEPLOYMENT (Implantação) no Azure AI Studio
endpoint = "https://marcelomaffeis-05082026-resource.services.ai.azure.com/&quot;
As informações podem ser inseridas no código por se tratar de um estudo acadêmico
3. Upload de Arquivos e Sistema RAG:
Adicione um componente st.file_uploader na barra lateral permitindo o envio de arquivos (PDF e TXT).
Implemente a lógica de extração do texto desse arquivo.
Implemente um sistema RAG (Retrieval-Augmented Generation) básico: quando o usuário fizer uma pergunta, o bot deve usar o texto do arquivo carregado como contexto para gerar a resposta.
4. Lógica de Chat:
Utilize st.chat_message e st.chat_input para a interface de mensagens.
Mantenha o histórico da conversa salvo no st.session_state.
Por favor, forneça o código completo, bem comentado, e inclua um bloco explicativo de quais bibliotecas (pip install) o usuário precisará instalar antes de rodar o código (ex: streamlit, openai, PyPDF2, etc)."

Será guardado no GitHub com o Streamlit e preciso do arquivo de requerimentos
