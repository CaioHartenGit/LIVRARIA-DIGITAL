from apps.schemas.livro_schemas import LivroCreate

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