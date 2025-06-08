import time
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# Caminho para o arquivo de credenciais do Google Cloud
credentials_path = 'dataset-21ffc933be35.json'

# Configurações para autenticar no Google Cloud e acessar o BigQuery
credentials = service_account.Credentials.from_service_account_file(credentials_path)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# Nome do dataset e tabela no BigQuery
dataset_id = 'dataset.datasetp8'
table_id = f'{dataset_id}.relatorios'

# Função para criar o dataset se ele não existir
def cria_dataset_se_nao_existir(client, dataset_id):
    try:
        client.get_dataset(dataset_id)  # Verifica se o dataset já existe
        print(f"Dataset {dataset_id} já existe.")
    except Exception:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"  # Define a localização do dataset (ajuste se necessário)

        # Cria o dataset
        dataset = client.create_dataset(dataset, exists_ok=True)  
        print(f"Dataset {dataset_id} criado com sucesso.")

# Função para criar a tabela se ela não existir
def cria_tabela_se_nao_existir(client, table_id):
    try:
        client.get_table(table_id)  # Verifica se a tabela já existe
        print(f"Tabela {table_id} já existe.")
    except Exception:
        # Esquema da tabela
        schema = [
            bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("conteudo", "STRING", mode="REQUIRED"),
        ]
        
        # Configuração da tabela
        table = bigquery.Table(table_id, schema=schema)

        # Cria a tabela
        table = client.create_table(table)  
        print(f"Tabela {table_id} criada com sucesso.")
        
        # Aguarda alguns segundos para garantir que a tabela foi propagada corretamente
        time.sleep(5)

# Cria o dataset se ele não existir
cria_dataset_se_nao_existir(client, dataset_id)

# Cria a tabela se ela não existir
cria_tabela_se_nao_existir(client, table_id)

# Dados de exemplo para inserção
dados_exemplo = [
    {"id": 1, "conteudo": "A receita líquida da empresa TechCorp cresceu 12% no último trimestre, impulsionada pelo aumento das vendas online."},
    {"id": 2, "conteudo": "A análise de mercado revelou que 45% dos consumidores preferem produtos com integração IoT, indicando uma tendência de crescimento nesse segmento."},
    {"id": 3, "conteudo": "A expansão internacional para a América Latina mostrou-se viável, com um retorno projetado de 18% sobre o investimento inicial em cinco anos."},
    {"id": 4, "conteudo": "As vendas do segundo trimestre caíram 8%, principalmente devido à baixa demanda sazonal e à concorrência agressiva."},
    {"id": 5, "conteudo": "O plano estratégico aponta que a diversificação de produtos digitais pode aumentar a participação de mercado em até 25% nos próximos três anos."},
    {"id": 6, "conteudo": "A análise SWOT identificou a dependência de um fornecedor específico como uma fraqueza crítica, sugerindo a necessidade de diversificação da cadeia de suprimentos."},
    {"id": 7, "conteudo": "A pesquisa de satisfação mostrou que 78% dos clientes estão satisfeitos com o atendimento ao cliente, mas há oportunidades de melhoria no tempo de resposta."},
    {"id": 8, "conteudo": "A auditoria interna revelou que 10% das transações não seguiram os protocolos de conformidade, exigindo uma revisão dos processos operacionais."},
    {"id": 9, "conteudo": "A implementação do ERP resultou em uma redução de 15% nos custos operacionais, mas houve resistência inicial dos colaboradores, necessitando maior treinamento."},
    {"id": 10, "conteudo": "As campanhas de marketing digital geraram um aumento de 30% no tráfego do site, porém, a conversão para vendas diretas ainda está abaixo da meta esperada."}
]

# Convertendo os dados para um DataFrame
df = pd.DataFrame(dados_exemplo)

# Inserindo os dados na tabela do BigQuery
try:
    job = client.load_table_from_dataframe(df, table_id)
    job.result()  # Aguarda a conclusão do job
    print("Dados inseridos com sucesso na tabela.")
except Exception as e:
    print(f"Erro ao inserir os dados: {e}")