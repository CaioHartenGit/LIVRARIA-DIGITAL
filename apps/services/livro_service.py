from apps.schemas.livro_schemas import LivroCreate
# pyrefly: ignore[missing-import]
import fitz
import base64
import os
import shutil

class LivroService:
    def __init__(self, livro_repository, usuario_repository):
        self.livro_repository = livro_repository
        self.usuario_repository = usuario_repository

    def obter_fatias_paginas(self, documento_pdf):
        fatias = []
        for indice_pagina in range(len(documento_pdf)):
            rect = documento_pdf[indice_pagina].rect
            largura = rect.width
            altura = rect.height

            # Se o PDF for uma tira vertical gigante (ex: Mangá/Webtoon salvo de site em 1 página)
            if largura > 0 and altura > largura * 2.2:
                altura_fatia = largura * 1.45
                y_atual = 0.0
                while y_atual < altura:
                    y_fim = min(y_atual + altura_fatia, altura)
                    if (altura - y_fim) < (altura_fatia * 0.25):
                        y_fim = altura
                    fatias.append((indice_pagina, fitz.Rect(0, y_atual, largura, y_fim)))
                    y_atual = y_fim
            else:
                fatias.append((indice_pagina, rect))
        return fatias

    def salvar_arquivo_pdf(self, arquivo):
        if not arquivo.filename or not arquivo.filename.lower().endswith(".pdf"):
            raise ValueError("O arquivo enviado deve ser um PDF")

        os.makedirs("uploads", exist_ok = True)
        caminho_arquivo = f"uploads/{arquivo.filename}"

        with open(caminho_arquivo, "wb") as buffer:
            shutil.copyfileobj(arquivo.file, buffer)

        documento_pdf = fitz.open(caminho_arquivo)
        fatias = self.obter_fatias_paginas(documento_pdf)
        total_paginas = max(1, len(fatias))
        documento_pdf.close()
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
        if not os.path.exists(livro["arquivo_path"]):
            raise ValueError("Arquivo do livro não encontrado no servidor. Envie o PDF novamente.")

        documento_pdf = fitz.open(livro["arquivo_path"])
        fatias = self.obter_fatias_paginas(documento_pdf)
        total_paginas_real = max(1, len(fatias))

        if pagina < 1 or pagina > total_paginas_real:
            documento_pdf.close()
            raise ValueError("Número de página inválido para este livro")

        indice_fisico, rect_fatia = fatias[pagina - 1]
        pagina_visual = documento_pdf[indice_fisico]
        texto = pagina_visual.get_text("text", clip=rect_fatia) or ""

        # Calcula escala segura para não estourar os 512MB de RAM do Render em páginas grandes
        largura_fatia = max(rect_fatia.width, 1.0)
        altura_fatia = max(rect_fatia.height, 1.0)
        escala = min(1.5, 950.0 / largura_fatia, 1800.0 / altura_fatia)

        pixmap = pagina_visual.get_pixmap(matrix=fitz.Matrix(escala, escala), clip=rect_fatia, alpha=False)
        imagem_base64 = base64.b64encode(pixmap.tobytes("jpeg", jpg_quality=82)).decode("utf-8")
        documento_pdf.close()

        return {
                "id_livro": livro["id"],
                "titulo": livro["titulo"],
                "pagina_atual": pagina,
                "total_paginas": total_paginas_real,
                "texto": texto,
                "imagem_base64": f"data:image/jpeg;base64,{imagem_base64}"
                }