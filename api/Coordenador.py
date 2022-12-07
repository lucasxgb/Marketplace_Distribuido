# -*- coding: utf-8 -*-
from pydantic import BaseModel

## Classe criada aqui mas colocar em arquivo separado
class Coordenador(BaseModel):
    existeCoordenador: bool
    nomeCoordenador: str
    souCoordenador : bool
    jaVotou : bool
    votoMarktplace01 : bool
    votoMarktplace02 : bool
    votoMarktplace03 : bool