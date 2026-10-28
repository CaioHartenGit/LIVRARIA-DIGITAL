from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
# ==================================================================================
# Criando Livro Create
# ==================================================================================
class LivroCreate(BaseModel):
    titulo: str = Field( min_length = 1, max_length = 200, description = "Titulo do livro")
    autor: str = Field( min_length = 1, max_length = 100, description = "Autor do livro")
    total_paginas: int = Field(gt = 0, description = "Total de páginas do livro")
    arquivo_path: str = Field(min_length = 1, max_length = 255, description = "Caminho do arquivo do livro")
    usuario_id: int = Field(gt = 0, description = "ID do usuário que cadastrou o livro")



# ==================================================================================
# Criando Livro Response
# ==================================================================================
class LivroResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id: int
    titulo: str
    autor: str
    total_paginas: int
    arquivo_path: str
    ativo: bool
    usuario_id: Optional[int] = None






