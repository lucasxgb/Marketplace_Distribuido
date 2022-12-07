# -*- coding: utf-8 -*-
from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

# Instalações
# pip install fastapi
# pip install uvicorn


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




# Listar todos os produtos do carrinho
@app.get("/produtosCarrinho/{nome}")
def listagem(nome : str):
    # Abrir banco
    with open("banco/carrinho.json", 'r' , encoding='utf-8') as database:
        clientes = json.load(database)
    # Colocar nome da loja e retornar o Json
    return {"Marketplace 01" : clientes[nome.lower()]}




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
    produtos[produto.nome.lower()] = {"preco" : produto.preco, "quantidade" : produto.quantidade, "linkImagem" : produto.linkImagem.lower()}
    # Escrever banco com os dados mudados
    with open("banco/produtos.json", 'w' , encoding='utf-8') as database:
        json.dump(produtos, database, indent=4)  
    # Retornar mensagem de sucesso
    return {"message" : "Sucesso" }




# Colocar carrinho
@app.put("/carrinho")
def carrinho(produto : ProdutoCadastrar, nome : str):
    prod = {}
    # Abrir banco
    with open("banco/carrinho.json", 'r' , encoding='utf-8') as database:
        clientes = json.load(database)
    # Adicionar produto ao carrinho
    prod[produto.nome.lower()] = {"preco" : produto.preco, "quantidade" : produto.quantidade, "linkImagem" : produto.linkImagem.lower()}
    clientes[nome.lower()][produto.nome.lower() ] = prod[produto.nome.lower()]
    # Escrever banco com os dados mudados
    with open("banco/carrinho.json", 'w' , encoding='utf-8') as database:
        json.dump(clientes, database, indent=4)  
    
    return {"message" : "Adicionado ao carrinho com sucesso"}




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
