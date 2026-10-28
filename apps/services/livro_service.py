from apps.schemas.livro_schemas import LivroCreate
# pyrefly: ignore[missing-import]
from pypdf import PdfReader
# pyrefly: ignore[missing-import]
import fitz
import base64
import os
class LivroService:
    def __init__(self, livro_repository):
        self.livro_repository = livro_repository

    def cadastrar(self, titulo, autor, total_paginas, arquivo_path):
        livrocriar = LivroCreate(titulo = titulo, autor = autor, total_paginas = total_paginas, arquivo_path = arquivo_path)
        
        livrocadastrado = self.livro_repository.buscar_por_nome(livrocriar.titulo)
        if livrocadastrado:
            raise ValueError("Já existe um livro com esse título cadastrado")

        return self.livro_repository.cadastrar(
            livrocriar.titulo,
            livrocriar.autor,
            livrocriar.total_paginas,
            livrocriar.arquivo_path,
        )

    def listar_livro(self):
        lista = self.livro_repository.listar_livros()
        if not lista:
            raise ValueError("Não existem livros cadastrados")
        return lista

    def buscar_livro_por_id(self, id):
        livro = self.livro_repository.buscar_livro_por_id(id)
        if livro is None:
            raise ValueError("ID do livro não existe")
        return livro

    def buscar_por_nome(self, titulo):
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