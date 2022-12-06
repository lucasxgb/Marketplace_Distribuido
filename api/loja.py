# -*- coding: utf-8 -*-
from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

# Ligar o uvicorn
# python -m uvicorn loja:app --reload




# Listar todos os produtos
@app.get("/produtos")
def listagem():
    # Abrir banco
    with open("banco/produtos.json", 'r' , encoding='utf-8') as database:
        produtos = json.load(database)
    # Colocar nome da loja e retornar o Json
    return {"Marketplace 01" : produtos}
    




# Listar produtos por nome
@app.get("/produtos/{nome}")
def listagem_especifica(nome: str):
    filtroProdutos = {}
    # Abrir banco
    with open("banco/produtos.json", 'r' , encoding='utf-8') as database:
        produtos = json.load(database)
    # Filtrar produtos
    for produto in produtos.keys():
        if nome.lower() in produto:
            filtroProdutos[produto] = produtos[produto]
    # Colocar nome da loja e retornar o Json
    return {"Marketplace 01" : filtroProdutos}




# Cadastrar produto
## Classe criada aqui mas colocar em arquivo separado
class ProdutoCadastrar(BaseModel):
    nome: str
    preco: float
    quantidade : int
    linkImagem : str

@app.post("/produto")
def cadastro(produto : ProdutoCadastrar):
    # Abrir banco
    with open("banco/produtos.json", 'r' , encoding='utf-8') as database:
        produtos = json.load(database)
    # Escrever novo produto no banco
    produtos[produto.nome.lower()] = {"preco" : produto.preco.lower(), "quantidade" : produto.quantidade.lower(), "linkImagem" : produto.linkImagem.lower()}
    # Escrever banco com os dados mudados
    with open("banco/produtos.json", 'w' , encoding='utf-8') as database:
        json.dump(produtos, database, indent=4)  
    # Retornar mensagem de sucesso
    return {"message" : "Sucesso" }




# Fazer compra
@app.put("/comprar")
def comprar(produtosComprar : dict):
    # Abrir banco
    with open("banco/produtos.json", 'r' , encoding='utf-8') as database:
        produtos = json.load(database)
    # Reduzir o produto comprado
    for nomeProduto in produtosComprar.keys():
        produtos[nomeProduto.lower()]["quantidade"] -=  produtosComprar[nomeProduto]
    # Escrever banco com os dados mudados
    with open("banco/produtos.json", 'w' , encoding='utf-8') as database:
        json.dump(produtos, database, indent=4)  
    
    return {"message" : "Compra realizada com sucesso"}
