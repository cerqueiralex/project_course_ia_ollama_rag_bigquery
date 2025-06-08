# Chatbot de IA Generativa com RAG utilizando Ollama (LLama 3.2), Streamlit e Google BigQuery

Este projeto integra Google BigQuery, Streamlit, e modelos de linguagem generativa para criar uma aplicação interativa de análise de negócios baseada em IA. 

O primeiro script prepara o ambiente de dados, criando um dataset e uma tabela no BigQuery e inserindo relatórios corporativos com análises de desempenho, tendências de mercado e estratégias empresariais. 

O segundo script implementa uma interface web com Streamlit que permite ao usuário interagir em linguagem natural com esses dados. Utilizando RAG (Retrieval-Augmented Generation) com LlamaIndex, embeddings da HuggingFace e o modelo LLaMA 3, a aplicação transforma perguntas do usuário em consultas inteligentes, recupera informações relevantes do banco de dados e gera respostas detalhadas com base nos relatórios armazenados.

Tecnologias:  
* Python
  * Streamlit
  * Pandas  
* GCP - Bigquery
* Ollama
  * Modelo de LLM (Llama 3.2)

<img src="https://i.imgur.com/AYw4aOI.png" style="width:100%;height:auto"/>

Diagrama de desenvolvimento:
<img src="https://i.imgur.com/FIL4ThH.png" style="width:100%;height:auto"/>

## RAG (Retrieval-Augmented Generation)

É uma técnica que combina recuperação de informações com geração de texto por modelos de linguagem. Em vez de o modelo gerar respostas apenas com base no que foi treinado, o RAG permite que ele busque dados em fontes externas, como bancos de dados, documentos ou APIs, antes de produzir a resposta. 

Isso aumenta a precisão e atualidade das informações, pois o modelo passa a gerar respostas baseadas em dados realmente relevantes e atualizados, mesmo que não estivessem presentes no treinamento. 

O processo funciona de forma que o sistema recebe uma pergunta, busca trechos relevantes em uma base de dados, e depois usa o modelo de linguagem para gerar uma resposta utilizando esse conteúdo como contexto. *É uma forma eficaz de aplicar IA generativa em ambientes corporativos, onde as respostas precisam ser fundamentadas em informações específicas e seguras.*

## Modelo de Embeddings

Um modelo de embeddings é uma técnica de representação de dados que transforma palavras ou frases em vetores de números contínuos, capturando semelhanças e relações contextuais entre eles em um espaço multidimensional. Esses vetores permitem que palavras com significados semelhantes fiquem próximas entre si, facilitando o processamento e a análise de linguagem natural em algoritmos de aprendizado de máquina.

Esses modelos são essenciais para usar LLMs (Modelos de Linguagem de Grande Escala) porque traduzem dados textuais em uma forma numérica que o modelo consegue interpretar e processar. Os embeddings permitem que o LLM capture e compreenda nuances semânticas, como sinônimos ou contexto, melhorando a precisão e a relevância das respostas geradas pelo modelo.

Modelo que está sendo utilizado: HuggingFaceEmbeddings
```
from langchain_huggingface import HuggingFaceEmbeddings
```

## Instalando Dependências

Instalar todas as bibliotecas com as versões exatas (ou compatíveis) especificadas no arquivo.

O arquivo requirements.txt é específico para projetos Python. Ele é usado pelo pip (gerenciador de pacotes do Python) para instalar dependências listadas no projeto.

```
pip install -r requirements.txt
```
## Gerando Chave de API Json para conexão ao Big Query:

Como baixar a chave JSON e conectar ao BigQuery
1. Acesse o Google Cloud Console: https://console.cloud.google.com/
2. Crie ou selecione um projeto (No topo da tela, clique no seletor de projetos e crie um novo projeto ou escolha um projeto existente.)
3. Ative a API do BigQuery (se ainda não estiver ativa) Vá para "APIs e serviços" > "Biblioteca" > Procure por BigQuery API e clique em "Ativar".
4. Crie uma conta de serviço:  Vá para "IAM e administrador" > "Contas de serviço" > Clique em "Criar conta de serviço".
5. Conceda permissões à conta de serviço: No mínimo, adicione o papel: BigQuery Data Editor (para inserir dados) / BigQuery Data Viewer (para visualizar)
6. Gere e baixe a chave JSON: Na lista de contas de serviço, clique na conta que você criou.

exemplo de arquivo
```
dataset-21ffc933be35.json
```

## Ollama e modelo Llama 3.2

Modelo utilizado:
https://ollama.com/library/llama3.2

1. Instalar Ollama
2. Instalar Llama 3.2

```
ollama run llama3.2
```

## Rodando a aplicação

Acessar diretório através do terminal
```
cd/project_course_ia_ollama_rag_bigquery/
```
```
streamlit run app.py
```
mac:8501

<img src="https://i.imgur.com/HMh4412.png" style="width:100%;height:auto"/>
