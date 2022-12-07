# -*- coding: utf-8 -*-
from pydantic import BaseModel

## Classe criada aqui mas colocar em arquivo separado
class ProdutoCadastrar(BaseModel):
    nome: str
    preco: float
    quantidade : int
    linkImagem : str