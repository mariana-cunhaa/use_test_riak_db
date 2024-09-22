import requests
import json
import connect_riak as cr

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
    Consulta um artigo usando a chave (name_bucket) e o título.
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

# Fazer a requisição GET para a API
response = requests.get(url, params={"filter": "title.search:machine learning", "per-page": 5}, verify=False)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    data = response.json()
    for work in data['results']:
        inserir_artigo(work)  
else:
    print(f"Erro na requisição: {response.status_code}")

# Listar as chaves no bucket "Artigos"
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
