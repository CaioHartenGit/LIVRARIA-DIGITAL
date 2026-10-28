from apps.schemas.livro_schemas import LivroCreate
# pyrefly: ignore[missing-import]
from pypdf import PdfReader
# pyrefly: ignore[missing-import]
import fitz
import base64
import os
class LivroService:
    def __init__(self, livro_repository, usuario_repository):
        self.livro_repository = livro_repository
        self.usuario_repository = usuario_repository

    def salvar_arquivo_pdf(self, arquivo):
        if not arquivo.filename or not arquivo.filename.lower().endswith(".pdf"):
            raise ValueError("O arquivo enviado deve ser um PDF")

        os.makedirs("uploads", exist_ok = True)
        caminho_arquivo = f"uploads/{arquivo.filename}"

        with open(caminho_arquivo, "wb") as buffer:
            buffer.write(arquivo.file.read())

        leitor = PdfReader(caminho_arquivo)
        total_paginas = len(leitor.pages)
        return caminho_arquivo, total_paginas

    def cadastrar(self, titulo, autor, total_paginas, arquivo_path, usuario_id):
        livrocriar = LivroCreate(
            titulo = titulo,
            autor = autor,
            total_paginas = total_paginas,
            arquivo_path = arquivo_path,
            usuario_id = usuario_id
        )

        usuario = self.usuario_repository.buscar_usuario_por_id(livrocriar.usuario_id)
        if usuario is None:
            raise ValueError("Usuário informado não existe")

        livrocadastrado = self.livro_repository.buscar_por_nome_e_usuario(livrocriar.titulo, livrocriar.usuario_id)
        if livrocadastrado:
            raise ValueError("Você já cadastrou um livro com esse título")

        return self.livro_repository.cadastrar(
            livrocriar.titulo,
            livrocriar.autor,
            livrocriar.total_paginas,
            livrocriar.arquivo_path,
            livrocriar.usuario_id
        )

    def cadastrar_com_upload(self, titulo, autor, usuario_id, arquivo):
        caminho_arquivo, total_paginas = self.salvar_arquivo_pdf(arquivo)
        return self.cadastrar(
            titulo = titulo,
            autor = autor,
            total_paginas = total_paginas,
            arquivo_path = caminho_arquivo,
            usuario_id = usuario_id
        )

    def listar_livro(self, usuario_id=None):
        if usuario_id is not None:
            usuario = self.usuario_repository.buscar_usuario_por_id(usuario_id)
            if usuario is None:
                raise ValueError("Usuário não encontrado")

            if usuario["tipo_usuario"] == "admin":
                lista = self.livro_repository.listar_livros()
            else:
                lista = self.livro_repository.listar_livros_por_usuario(usuario_id)
        else:
            lista = self.livro_repository.listar_livros()

        if not lista:
            raise ValueError("Não existem livros cadastrados")
        return lista

    def buscar_livro_por_id(self, id):
        livro = self.livro_repository.buscar_livro_por_id(id)
        if livro is None:
            raise ValueError("ID do livro não existe")
        return livro

    def buscar_por_nome(self, titulo, usuario_id=None):
        if usuario_id is not None:
            usuario = self.usuario_repository.buscar_usuario_por_id(usuario_id)
            if usuario is None:
                raise ValueError("Usuário não encontrado")

            if usuario["tipo_usuario"] == "admin":
                livro = self.livro_repository.buscar_por_nome(titulo)
            else:
                livro = self.livro_repository.buscar_por_nome_e_usuario(titulo, usuario_id)
        else:
            livro = self.livro_repository.buscar_por_nome(titulo)

        if not livro:
            raise ValueError("Título do livro não existe")
        return livro

    def deletar_livro(self, id):
        delete = self.livro_repository.deletar_livro(id)
        if delete is None:
            raise ValueError("ID do livro não existe para ser deletado")
        return delete

    
    def ler_pagina_livro(self,id,pagina):
        livro = self.livro_repository.buscar_livro_por_id(id)
        if livro is None:
            raise ValueError("ID do livro não existe")
        if pagina < 1 or pagina > livro["total_paginas"]:
            raise ValueError("Número de página inválido para este livro")
        if not os.path.exists(livro["arquivo_path"]):
            raise ValueError("Arquivo do livro não encontrado")
    
        leitor = PdfReader(livro["arquivo_path"])
        texto = leitor.pages[pagina - 1].extract_text() or ""

        # Renderiza a página como imagem (para Mangás, HQs e PDFs ilustrados)
        documento_pdf = fitz.open(livro["arquivo_path"])
        pagina_visual = documento_pdf[pagina - 1]
        pixmap = pagina_visual.get_pixmap(matrix=fitz.Matrix(1.6, 1.6))
        imagem_base64 = base64.b64encode(pixmap.tobytes("png")).decode("utf-8")
        documento_pdf.close()

        return {
                "id_livro": livro["id"],
                "titulo": livro["titulo"],
                "pagina_atual": pagina,
                "total_paginas": livro["total_paginas"],
                "texto": texto,
                "imagem_base64": f"data:image/png;base64,{imagem_base64}"
                }