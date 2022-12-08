# -*- coding: utf-8 -*-
from fastapi import FastAPI
import json
from ProdutoCadastrar import ProdutoCadastrar
from Coordenador import Coordenador
import requests
from time import sleep
from random import randint
from fastapi.middleware.cors import CORSMiddleware
import threading



app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Instalações
# pip install fastapi
# pip install uvicorn
# pip install requests


# Ligar o uvicorn
# python -m uvicorn mark01:app --reload --port=5000

coordenador = Coordenador
coordenadorOnline = False

# Listar todos os produtos
@app.get("/produtos")
def listagem():
    # Abrir banco
    with open("banco/produtosM2.json", 'r' , encoding='utf-8') as database:
        produtos = json.load(database)
    # Colocar nome da loja e retornar o Json
    return {"Marketplace02" : produtos}
    




# Listar produtos por nome
@app.get("/produtos/{nome}")
def listagem_especifica(nome: str):
    filtroProdutos = {}
    # Abrir banco
    with open("banco/produtosM2.json", 'r' , encoding='utf-8') as database:
        produtos = json.load(database)
    # Filtrar produtos
    for produto in produtos.keys():
        if nome.lower() in produto:
            filtroProdutos[produto] = produtos[produto]
    # Colocar nome da loja e retornar o Json
    return {"Marketplace02" : filtroProdutos}




# Listar todos os produtos do carrinho
@app.get("/produtosCarrinho/{nome}")
def listagem(nome : str):
    # Abrir banco
    with open("banco/carrinhoM2.json", 'r' , encoding='utf-8') as database:
        clientes = json.load(database)
    # Colocar nome da loja e retornar o Json
    return {"Marketplace02" : clientes[nome.lower()]}




# Cadastrar produto
@app.post("/produto")
def cadastro(produto : ProdutoCadastrar):
    # Abrir banco
    with open("banco/produtosM2.json", 'r' , encoding='utf-8') as database:
        produtos = json.load(database)
    # Escrever novo produto no banco
    produtos[produto.nome.lower()] = {"preco" : produto.preco, "quantidade" : produto.quantidade, "linkImagem" : produto.linkImagem.lower()}
    # Escrever banco com os dados mudados
    with open("banco/produtosM2.json", 'w' , encoding='utf-8') as database:
        json.dump(produtos, database, indent=4)  
    # Retornar mensagem de sucesso
    return {"message" : "Sucesso" }




# Colocar carrinho
@app.put("/carrinho")
def carrinho(produto : ProdutoCadastrar, nome : str):
    prod = {}
    # Abrir banco
    with open("banco/carrinhoM2.json", 'r' , encoding='utf-8') as database:
        clientes = json.load(database)
    # Adicionar produto ao carrinho
    prod[produto.nome.lower()] = {"preco" : produto.preco, "quantidade" : produto.quantidade, "linkImagem" : produto.linkImagem.lower()}
    clientes[nome.lower()][produto.nome.lower() ] = prod[produto.nome.lower()]
    # Escrever banco com os dados mudados
    with open("banco/carrinhoM2.json", 'w' , encoding='utf-8') as database:
        json.dump(clientes, database, indent=4)  
    
    return {"message" : "Adicionado ao carrinho com sucesso"}




# Fazer compra
@app.put("/comprar")
def comprar(produtosComprar : dict):
    # Abrir banco
    with open("banco/produtosM2.json", 'r' , encoding='utf-8') as database:
        produtos = json.load(database)
    # Reduzir o produto comprado
    for nomeProduto in produtosComprar.keys():
        if produtos[nomeProduto.lower()]["quantidade"] >= produtosComprar[nomeProduto]:
            produtos[nomeProduto.lower()]["quantidade"] -=  produtosComprar[nomeProduto]
        else:
            return {"message" : "Compra negada"}
    # Escrever banco com os dados mudados
    with open("banco/produtosM2.json", 'w' , encoding='utf-8') as database:
        json.dump(produtos, database, indent=4) 
    
    return {"message" : "Compra realizada com sucesso"}




# ==========================================================================



# Fazer uma Thread para ficar mandando mensagem para as outras APIs
    # Colocar um tempo ramdomico para mandar mensagem pedindo permissão para ser o coordenador
        # Se não conseguir eleger nenhum coordenador, pedir novamente atráves de um tempo ramdomico
    # Verificar se o coordenador está no ar, se não estiver pedir para ser o coordenador
        # Se não conseguir, verificar se já tem coordenador, e pedir para ser novamente depois de um tempo




# Pedir para ser coordenador
def pedir_para_ser_coordenador():
    global coordenadorOnline
    print("=============== Pendindo para ser coordenador ======================")
    print(f"=================== {coordenador.nomeCoordenador} ==================")
    print(f"=================== {coordenadorOnline} ==================")
    #Mandar mensagem para os 3 marketplaces com o padrão 
        # "/eleicao/marketplace01"
        # "/eleicao/marketplace02"
        # "/eleicao/marketplace03"
    if coordenadorOnline != True:
        pedidoMarket01 = requests.post("localhost:4000/eleicao/marketplace01") 
        pedidoMarket02 = requests.post("localhost:5000/eleicao/marketplace02")
        pedidoMarket03 = requests.post("localhost:8000/eleicao/marketplace03")

        aprovacoes = 0

        if pedidoMarket01 == True:
            aprovacoes += 1
        if pedidoMarket02 == True:
            aprovacoes += 1
        if pedidoMarket03 == True:
            aprovacoes += 1

        if aprovacoes >= 1.5:
            # Eleger esse como o coordenador 
            coordenador.existeCoordenador = True
            coordenador.nomeCoordenador = "Marktplace02"
            coordenador.souCoordenador = True
            # Avisar aos outros
            #Mandar mensagem para os 3 marketplaces com o padrão 
                # "/eleicao/marketplace01"
                # "/eleicao/marketplace02"
                # "/eleicao/marketplace03"
            requests.post("localhost:4000/coordenador/eleito/marketplace01") #Market01
            requests.post("localhost:8000/coordenador/eleito/marketplace03") #Market02
            return {"coordendador" : "marketplace01"}
        else:
            coordenador.jaVotou = False
            coordenador.votoMarktplace01 = False
            coordenador.votoMarktplace02 = False
            coordenador.votoMarktplace03 = False
            # Verificar se ja existe coordenador, se não, pedir novamente depois de um tempo
            if coordenador.existeCoordenador == False:
                tempoEspera = randint(1,20) * 0.1
                sleep(tempoEspera)
                pedir_para_ser_coordenador()
            else:
                return {"coordendador" : coordenador.nomeCoordenador}
    else:
        return {"coordendador" : coordenador.nomeCoordenador}
        




# Verificar se o coordenador está online
def verificar_coordenador_online():
    sleep(10)
    #Mandar mensagem para o coordenador
        # "/eleicao/{coordenador}"
    global coordenadorOnline
    coordenadorOnline = False
    if coordenador.souCoordenador == True:
        coordenadorOnline = True
    if coordenador.nomeCoordenador == "Marktplace01":
        coordenadorOnline = requests.get("localhost:4000/coordenador/online")
    elif coordenador.nomeCoordenador == "Marktplace03":
        coordenadorOnline = requests.get("localhost:8000/coordenador/online")





# Votar em um market para ser o coordenador
@app.post("/eleicao/{marketplace}")
def eleger(marketplace : str):
    if coordenador.existeCoordenador == True:
        return False
    else:
        if coordenador.jaVotou == True: #Verificar se esse processo já deu seu voto
            return False
        else:
            if marketplace == "Marktplace01":
                coordenador.votoMarktplace01 = True
            elif marketplace == "Marktplace02":
                coordenador.votoMarktplace02 = True
            elif marketplace == "Marktplace03":
                coordenador.votoMarktplace03 = True
            else:
                return False
            
            coordenador.jaVotou = True
            return True




# receber nome do market coordenador
@app.post("/coordenador/eleito/{marketplace}")
def eleito(marketplace : str):
    coordenador.jaVotou = False
    coordenador.votoMarktplace01 = False
    coordenador.votoMarktplace02 = False
    coordenador.votoMarktplace03 = False
    coordenador.existeCoordenador = True
    coordenador.nomeCoordenador = marketplace
    if marketplace != "marketplace02":
        coordenador.souCoordenador = False

  


# Dizer que estou online
@app.get("/coordenador/online")
def online():
    return True




# Thread para ficar pedindo pra ser o coordenador

threading.Thread(target=pedir_para_ser_coordenador, args=[])
threading.Thread(target=verificar_coordenador_online, args=[])
