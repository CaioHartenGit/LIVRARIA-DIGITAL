from fastapi import APIRouter, status, HTTPException, UploadFile, File, Form
import os
# pyrefly: ignore[missing-import]
from pypdf import PdfReader
from apps.schemas.livro_schemas import LivroCreate, LivroResponse
from apps.repository.livro_repository import LivroRepository
from apps.services.livro_service import LivroService
from typing import List, Literal

livro_repository = LivroRepository()
livro_service = LivroService(livro_repository)

router = APIRouter(prefix = "/livros", tags = ["Livros"])

# Criando Livros (com Upload Real de PDF)
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = LivroResponse)
def cadastrar_livros(
    titulo: str = Form(...),
    autor: str = Form(...),
    arquivo: UploadFile = File(...)
):
    try:
        if not arquivo.filename.endswith(".pdf"):
            raise ValueError("O arquivo enviado deve ser um PDF")

        os.makedirs("uploads", exist_ok = True)
        caminho_arquivo = f"uploads/{arquivo.filename}"

        with open(caminho_arquivo, "wb") as buffer:
            buffer.write(arquivo.file.read())

        leitor = PdfReader(caminho_arquivo)
        total_paginas = len(leitor.pages)

        cadastro_livro = livro_service.cadastrar(
            titulo,
            autor,
            total_paginas,
            caminho_arquivo
        )
        return cadastro_livro
    except ValueError as erro:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(erro)
        )

# Listando Livros
@router.get("/", response_model = List [LivroResponse])
def listar_livros():
    try:
        listar_livro = livro_service.listar_livro()
        if listar_livro == []:
            return "Nenhum livro cadastrado"
        return listar_livro
    except ValueError as erro:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(erro)
        )

# Buscando Livro por ID
@router.get("/{id}", response_model = LivroResponse, status_code = 200)
def buscar_livro_por_id(id: int):
    try:
        livro_por_id = livro_service.buscar_livro_por_id(id)
        if livro_por_id is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Livro nao encontrado"
            )
        return livro_por_id
    except ValueError as erro:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(erro)
        )

# Buscar Livro por Titulo
@router.get("/titulo/{titulo}", response_model = List [LivroResponse], status_code = 200)
def buscar_livro_por_titulo(titulo: str):
    try:
        livro_por_titulo = livro_service.buscar_por_nome(titulo)
        if livro_por_titulo == []:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Livro nao encontrado"
            )
        return livro_por_titulo
    except ValueError as erro:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(erro)
        )

# Deletar livro
@router.delete("/{id}", status_code = 200)
def deletar_livro(id: int):
    try:
        livro_deletado = livro_service.deletar_livro(id)
        if livro_deletado is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Livro nao encontrado"
            )
        return "Livro deletado com sucesso"
    except ValueError as erro:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(erro)
        )

# Ler Pagina (AUDIOBOOK)
@router.get("/{id}/pagina/{pagina}", response_model = dict, status_code = 200)
def ler_pagina(id: int, pagina: int):
    try:
        pagina_lida = livro_service.ler_pagina_livro(id, pagina)
        return pagina_lida
    except ValueError as erro:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(erro)
        )
    