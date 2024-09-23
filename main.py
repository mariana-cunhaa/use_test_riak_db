import requests
import json
import connect_riak as cr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# URL da API OpenAlex
url = "https://api.openalex.org/works"

def inserir_artigo(work):
    """
    Insere um artigo no Riak
    """
    entry = {
        'title': work.get('title'),
        'relevance_score': work.get('relevance_score'),
        'publication_year': work.get('publication_year'),
        'publication_date': work.get('publication_date'),
        'id_mag': work.get('ids', {}).get('mag')
    }
    cr.inserir("Artigos", work['title'], json.dumps(entry))

def consultar_artigo(name_bucket, chave):
    """
    Consulta um artigo usando a chave e o título.
    """
    artigo = cr.consultar(name_bucket, chave)
    if artigo:
        print(f"Artigo encontrado: ")
        print(artigo)
    else:
        print("Artigo não encontrado.")

def deletar_artigo(name_bucket, chave):
    """
    Deleta o objeto com a chave fornecida.
    """
    artigo_excluido = cr.deletar(name_bucket, chave)  
    if artigo_excluido:
        print(f"Objeto excluído com sucesso: Chave: {chave}.")
    else:
        print(f"O objeto com a chave: {chave} não foi encontrado.")

def listar_chaves(name_bucket):
    """
    Lista todas as chaves de um bucket no Riak
    """
    bucket = cr.conectar_riak(name_bucket) 
    keys = bucket.get_keys()  
    return keys


def gerar_relatorio_graficos(name_bucket):
    """
    Gera relatórios gráficos dos dados armazenados no Riak.
    """
    keys = listar_chaves(name_bucket)

    artigos = []

    # Consulta todos os artigos no bucket
    for chave in keys:
        artigo = cr.consultar(name_bucket, chave)
        if artigo:
            artigos.append(json.loads(artigo)) 

    if artigos:
        df = pd.DataFrame(artigos)

        # Gráfico de distribuição de artigos por ano de publicação
        plt.figure(figsize=(10, 6))
        sns.countplot(x='publication_year', data=df, palette='viridis')
        plt.title('Distribuição de Artigos por Ano de Publicação')
        plt.xlabel('Ano de Publicação')
        plt.ylabel('Número de Artigos')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # Gráfico de Relevance Score por Ano
        plt.figure(figsize=(10, 6))
        sns.barplot(x='publication_year', y='relevance_score', data=df, palette='magma')
        plt.title('Relevance Score por Ano de Publicação')
        plt.xlabel('Ano de Publicação')
        plt.ylabel('Relevance Score Médio')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    else:
        print("Nenhum dado disponível para gerar gráficos.")
    
# Faz a requisição GET para a API
response = requests.get(url, 
                        params={"filter": "title.search:machine learning", "per-page": 100}, verify=False)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    data = response.json()
    for work in data['results']:
        inserir_artigo(work)  
else:
    print(f"Erro na requisição: {response.status_code}")

# Lista as chaves no bucket "Artigos"
chaves = listar_chaves("Artigos")
print("Chaves encontradas no bucket 'Artigos': \n")
for chave in chaves:
    print(chave)

# Teste de exemplo
print("\n")
consultar_artigo("Artigos", "UCI Machine Learning Repository")
print("\n")
deletar_artigo("Artigos", "UCI Machine Learning Repository")
print("\n")
consultar_artigo("Artigos", "UCI Machine Learning Repository")
print("\n")
deletar_artigo("Artigos", "Machine learning: An artificial intelligence approach")
deletar_artigo("Artigos", "Foundations of Machine Learning")
print("\n")
gerar_relatorio_graficos("Artigos")