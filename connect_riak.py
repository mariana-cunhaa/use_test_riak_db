import riak

def conectar_riak(name_bucket):
    """
    Conecta ao Riak KV e acessa o bucket especificado
    """
    client = riak.RiakClient(pb_port=8087, protocol='pbc')
    return client.bucket(name_bucket)

def inserir(name_bucket, chave, valor):
    """
    Insere um novo objeto no bucket
    """
    bucket = conectar_riak(name_bucket)
    obj = bucket.new(chave, data=valor)
    obj.store()
    print(f"Objeto inserido: Chave: {chave}, Valor: {valor}")
    print("\n")

def consultar(name_bucket, chave):
    """
    Consulta e retorna os objetos com as chaves fornecidas.
    """
    bucket = conectar_riak(name_bucket)
    obj = bucket.get(chave)
    if obj.exists:
        print(f"Chave: {chave}")
        return obj.data
    else:
        print(f"Chave: {chave} não encontrada.")
        return None

def deletar(name_bucket, chave):
    """
    Deleta o objeto com a chave fornecida.
    Retorna True se o objeto foi excluído, False se não foi encontrado.
    """
    bucket = conectar_riak(name_bucket)
    obj = bucket.get(chave)
    if obj.exists:
        obj.delete()
        return True
    else:
        return False