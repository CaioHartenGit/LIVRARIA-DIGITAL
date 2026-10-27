from pydantic import BaseModel, Field, ConfigDict


# Criando Classe UsuarioCreate
class UsuarioCreate(BaseModel):
    nome: str = Field(min_length = 1, max_length = 100, description = "Nome do usuário")
    email: str = Field(min_length = 1, max_length = 100, description = "Email do usuário")
    senha: str = Field(min_length = 1, max_length = 100, description = "Senha do usuário")

# Criando Classe UsuarioLogin
class UsuarioLogin(BaseModel):
    email: str = Field(min_length = 1, max_length = 100, description = "Email do usuário")
    senha: str = Field(min_length = 1, max_length = 100, description = "Senha do usuário")
    
# Criando Classe UsuarioResponse
class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id: int
    nome: str
    email: str
    ativo: bool
    tipo_usuario: str
