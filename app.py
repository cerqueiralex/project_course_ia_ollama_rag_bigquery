import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings  
from llama_index.llms.ollama import Ollama  
from llama_index.core import VectorStoreIndex, Settings, Document
from langchain_community.chat_message_histories import ChatMessageHistory
from google.cloud import bigquery
from google.oauth2 import service_account
import warnings
warnings.filterwarnings('ignore')

# Caminho para o arquivo de credenciais JSON doo BigQuery
credentials_path = "dataset-21ffc933be35.json"

# Define o LLM (Large Language Model)
llm = Ollama(model="llama3.2", request_timeout=600.0)

# Define o modelo de embeddings
embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Configurando o título da página e outras configurações (favicon)
st.set_page_config(page_title="IA Generativa com Ollama, LLM, RAG e Google BigQuery", page_icon=":100:", layout="centered")

# Define o título da aplicação
st.title("IA Generativa com Ollama, LLM, RAG e Google BigQuery")  
st.title("Análise de Negócios Baseada em IA Generativa com Ollama, LLM, RAG e Google BigQuery")

# Inicializa a sessão de mensagens se não existir
if "messages" not in st.session_state.keys():  
    st.session_state.messages = [
        {"role": "assistant", "content": "Digite sua pergunta"}
    ]

# Função para conectar ao BigQuery e extrair os dados
def carregar_dados_do_bigquery():
    
    # Autenticação usando o arquivo de credenciais
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # SQL para buscar os dados dos relatórios
    query = """
    SELECT id, conteudo
    FROM `dataset.datasetp8.relatorios`
    """
    
    # Executa a query
    query_job = client.query(query)
    result = query_job.result()
    
    # Coleta os resultados como uma lista de dicionários
    documentos = [{"id": row.id, "conteudo": row.conteudo} for row in result]

    return documentos

# Função para o Módulo de RAG com LlamaIndex, cacheada pelo Streamlit
@st.cache_resource(show_spinner=False)
def modulo_rag():
    with st.spinner(text="Carregando e indexando os documentos do BigQuery – aguarde!"):
        
        # Carrega os dados do BigQuery
        documentos = carregar_dados_do_bigquery()

        # Cria uma lista de objetos de documento com base nos dados extraídos
        docs = [Document(text=doc["conteudo"], doc_id=str(doc["id"])) for doc in documentos]

        # Configura o LLM e o modelo de embeddings nos settings globais
        Settings.llm = llm
        Settings.embed_model = embed_model
        
        # Cria um índice de vetores a partir dos documentos
        index = VectorStoreIndex.from_documents(docs)
        
        return index

# Carrega o índice de dados
index = modulo_rag()

# Inicializa o motor de chat se não estiver na sessão
if "chat_engine" not in st.session_state.keys():  
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

# Verifica se há uma entrada de chat do usuário
if prompt := st.chat_input("Sua pergunta"):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Exibe as mensagens na interface de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Gera uma resposta se a última mensagem não for do assistente
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            user_message = st.session_state.messages[-1]["content"]
            contextual_prompt = f"Você é um analista de negócios especializado. O usuário fez a seguinte pergunta: '{user_message}'. Considere todos os relatórios disponíveis no banco de dados e forneça uma resposta detalhada e precisa."
            response = st.session_state.chat_engine.chat(contextual_prompt)
            st.write(response.response)
            st.session_state.messages.append({"role": "assistant", "content": response.response})


# Exemplos de perguntas para usar na aplicação:

# Qual a receita líquida da empresa TechCorp no último trimestre?
# Como foram as vendas do segundo trimestre?
# A implementação do ERP resultou em uma redução de custos operacionais?