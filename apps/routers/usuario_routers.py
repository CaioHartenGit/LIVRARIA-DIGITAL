from fastapi import APIRouter, status, HTTPException
from apps.schemas.usuario_schemas import UsuarioResponse, UsuarioCreate, UsuarioLogin
from apps.repository.usuario_repository import UsuarioRepository
from apps.services.usuario_service import UsuarioService
from typing import List

usuario_repository = UsuarioRepository()
usuario_service = UsuarioService(usuario_repository)

router = APIRouter(prefix = "/usuarios", tags = ["Usuarios"])

# Login de Usuario
@router.post("/login", status_code = status.HTTP_200_OK, response_model = UsuarioResponse)
def login_usuario(login_data: UsuarioLogin):
    try:
        usuario = usuario_service.login(login_data.email, login_data.senha)
        return usuario
    except ValueError as erro:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(erro)
        )

# Criando Usuario
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = UsuarioResponse)
def cadastrar_usuario(usuario_data: UsuarioCreate):
    try:
        cadastro_usuario = usuario_service.cadastrar(
            usuario_data.nome,
            usuario_data.email,
            usuario_data.senha
        )
        return cadastro_usuario
    except ValueError as erro:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(erro)
        )

# Atualizando Usuario
@router.put("/{id}", status_code = status.HTTP_200_OK, response_model = UsuarioResponse)
def atualizar_usuario(id: int, usuario_data: UsuarioCreate):
    try:
        usuario_atualizado = usuario_service.atualiza_usuario(
            usuario_data.nome,
            usuario_data.email,
            usuario_data.senha,
            id
        )
        return usuario_atualizado
    except ValueError as erro:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(erro)
        )

# Deletando Usuario
@router.delete("/{id_admin}", status_code = status.HTTP_204_NO_CONTENT)
def deletar_usuario(id_usuario: int, id_admin: int):
    try:
        usuario_service.deletar_usuario(id_usuario, id_admin)
    except PermissionError as erro:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = str(erro)
        )
    except ValueError as erro:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(erro)
        )

# Listando todos os usuarios (apenas para admin)
@router.get("/admin/{id}", status_code = status.HTTP_200_OK, response_model = List[UsuarioResponse])
def listar_todos_usuarios(id: int):
    try:
        usuarios = usuario_service.listar_tudo_admin(id)
        return usuarios
    except ValueError as erro:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(erro)
        )
        