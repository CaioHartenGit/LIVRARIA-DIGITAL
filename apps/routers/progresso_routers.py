from fastapi import APIRouter, status, HTTPException
from apps.schemas.progresso_schemas import ProgressoCreate, ProgressoResponse, ProgressoUpdate
from apps.repository.progresso_repository import ProgressoRepository
from apps.repository.usuario_repository import UsuarioRepository
from apps.repository.livro_repository import LivroRepository
from apps.services.progresso_service import ProgressoService
from typing import List, Literal


progresso_repository = ProgressoRepository()
usuario_repository = UsuarioRepository()
livro_repository = LivroRepository()
progresso_service = ProgressoService(progresso_repository, usuario_repository, livro_repository)

router = APIRouter(prefix = "/progresso", tags = ["Progresso"])

# Criando Progresso
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = ProgressoResponse)
def cadastrar_progresso(progresso_data: ProgressoCreate):
    try:
        cadastro_progresso = progresso_service.cadastrar_progresso(
            progresso_data.usuario_id,
            progresso_data.livro_id,
            progresso_data.pagina_atual
        )
        return cadastro_progresso
    except ValueError as erro:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(erro)
        )

# Atualizando Progresso
@router.put("/{usuario_id}/{livro_id}/", status_code = status.HTTP_200_OK, response_model = ProgressoResponse)
def atualizar_progresso(usuario_id: int, livro_id: int, progresso_data:ProgressoUpdate):
    try:
        progresso_atualizado = progresso_service.atualizar_pagina(
            usuario_id,
            livro_id,
            progresso_data.pagina_atual
        )
        return progresso_atualizado
    except ValueError as erro:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(erro)
        )

# Listar Progresso
@router.get("/{usuario_id}/", status_code = status.HTTP_200_OK, response_model = List[ProgressoResponse])
def listar_progresso(usuario_id: int):
    try:
        lista_progresso = progresso_service.listar_por_usuario(usuario_id)
        return lista_progresso
    except ValueError as erro:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(erro)
        )

# Deletar Progresso
@router.delete("/{id}/", status_code = status.HTTP_200_OK, response_model = ProgressoResponse)
def deletar_progresso(id: int):
    try:
        delete = progresso_service.deletar_progresso(id)
        return delete
    except ValueError as erro:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(erro)
        )