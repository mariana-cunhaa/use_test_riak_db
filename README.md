# Projeto: Gerenciamento de Artigos Acadêmicos com Riak e API OpenAlex

Este projeto tem como objetivo criar uma aplicação Python que interage com o banco de dados Riak, utilizando a API OpenAlex para extrair informações sobre artigos acadêmicos. A aplicação permite inserir, consultar, deletar e listar artigos em buckets do Riak.

## Estrutura do Projeto

- `connect_riak.py`: Contém funções para conectar ao Riak e realizar operações de CRUD (Create, Read, Update, Delete).
- `main.py`: Faz requisições à API OpenAlex, insere artigos no Riak, e permite consultar, deletar e listar artigos com base nos dados extraídos.

## Pré-requisitos

- Python 3.9 ou superior
- Docker
- Ambiente virtual Python (virtualenv ou pipenv)
- Pacote `requests` para realizar requisições à API

## Como Configurar e Executar o Projeto

### 1. Configurar o Ambiente Virtual

1. Abra o terminal e navegue até o diretório do projeto.
2. Crie um ambiente virtual com o comando:
   ```bash
   python -m venv venv
   ```
3. Ative o ambiente virtual:
     ```bash
     source venv/bin/activate
     ```

4. Instale as dependências:
   ```bash
   pip install requests riak
   ```

### 2. Criar e Rodar o Container Docker com Riak

1. **Baixar a imagem Docker do Riak**:
   Primeiro, faça o pull da imagem do Riak a partir do Docker Hub:
   ```bash
   docker pull basho/riak-kv
   ```

2. **Rodar o container**:
   Após baixar a imagem, execute o seguinte comando para criar e rodar o container Docker do Riak:
   ```bash
   docker run -d --name riak -p 8087:8087 basho/riak-kv
   ```

3. Verifique se o container está rodando corretamente:
   ```bash
   docker ps
   ```

### 3. Executar a Aplicação

1. No terminal, certifique-se de que o ambiente virtual está ativado e que o container Riak está rodando.
2. Execute o arquivo `main.py`:
   ```bash
   python main.py
   ```

A aplicação irá fazer uma requisição à API OpenAlex para buscar artigos relacionados ao termo "machine learning" e inseri-los no bucket `Artigos` do Riak. Além disso, ela listará as chaves no bucket e realizará operações de consulta e exclusão em um artigo específico.

### 4. Testar Operações no Riak

Após executar o script `main.py`, você pode testar as operações:

  
- Consultar um artigo:
   ```python
   consultar_artigo("Artigos", "Título do Artigo")
   ```

- Deletar um artigo:
   ```python
   deletar_artigo("Artigos", "Título do Artigo")
   ```

- Listar todas as chaves:
   ```python
   listar_chaves("Artigos")
   ```

## Observações

- O bucket utilizado para armazenar os artigos é chamado `Artigos`.
- A aplicação faz uma requisição à API OpenAlex para buscar até 50 artigos relacionados a "machine learning".
- O Riak precisa estar em execução na porta `8087` e configurado para o protocolo `Protocol Buffers`.
