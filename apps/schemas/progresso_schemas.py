from pydantic import BaseModel, Field, ConfigDict
from typing import Literal
from datetime import datetime


# Criando a Classe Progresso Create
class ProgressoCreate(BaseModel):
    usuario_id: int = Field(gt = 0, description= "ID do usuario")
    livro_id: int = Field(gt = 0, description= "ID do livro")
    pagina_atual: int = Field(ge = 0, description= "Página atual do usuário no livro")
    concluido: bool = Field(default = False, description= "Se o usuário concluiu o livro")


# Criando a classe Progresso UPDATE
class ProgressoUpdate(BaseModel):
    pagina_atual: int = Field(ge = 0, description= "Página atual do usuário no livro")
    


# Criando a classe Progresso Response
class ProgressoResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id: int
    usuario_id: int
    livro_id: int
    pagina_atual: int
    concluido: bool
    atualizado_em: datetime

