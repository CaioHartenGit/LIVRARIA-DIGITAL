class Livro:
    def __init__(self, id_livro, titulo, autor, total_paginas, arquivo_path, usuario_id=None, ativo=True):
        self.id_livro = id_livro
        self.titulo = titulo
        self.autor = autor
        self.total_paginas = total_paginas
        self.arquivo_path = arquivo_path
        self.usuario_id = usuario_id
        self.ativo = ativo

    @property
    def usuario_id(self):
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, NovoUsuarioId):
        if NovoUsuarioId is not None:
            if not isinstance(NovoUsuarioId, int) or isinstance(NovoUsuarioId, bool):
                raise ValueError("O ID do usuário dono do livro deve ser um número inteiro")
            if NovoUsuarioId <= 0:
                raise ValueError("O ID do usuário dono do livro deve ser maior que 0")
        self._usuario_id = NovoUsuarioId

    @property
    def id_livro(self):
        return self._id_livro

    @id_livro.setter
    def id_livro(self, NovoId):
        if NovoId is not None:
            if not isinstance(NovoId, int) or isinstance(NovoId, bool):
                raise ValueError("O ID do livro deve ser um número inteiro")
            if NovoId <= 0:
                raise ValueError("O ID do livro deve ser maior que 0")
        self._id_livro = NovoId

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, NovoTitulo):
        if not isinstance(NovoTitulo, str):
            raise ValueError("O título do livro deve ser uma string")
        NovoTitulo = NovoTitulo.strip()
        if NovoTitulo == "":
            raise ValueError("O título do livro não pode ser vazio")
        if len(NovoTitulo) < 3:
            raise ValueError("O título do livro deve ter pelo menos 3 caracteres")
        self._titulo = NovoTitulo

    @property
    def autor(self):
        return self._autor

    @autor.setter
    def autor(self, NovoAutor):
        if not isinstance(NovoAutor, str):
            raise ValueError("O autor do livro deve ser uma string")
        NovoAutor = NovoAutor.strip()
        if NovoAutor == "":
            raise ValueError("O autor do livro não pode ser vazio")
        if len(NovoAutor) < 3:
            raise ValueError("O autor do livro deve ter pelo menos 3 caracteres")
        self._autor = NovoAutor
    
    @property
    def total_paginas(self):
        return self._total_paginas

    @total_paginas.setter
    def total_paginas(self, NovoTotalPaginas):
        if not isinstance(NovoTotalPaginas, int) or isinstance(NovoTotalPaginas, bool):
            raise ValueError("O total de páginas deve ser um número inteiro")
        if NovoTotalPaginas <= 0:
            raise ValueError("O total de páginas deve ser maior que 0")
        self._total_paginas = NovoTotalPaginas
    
    @property
    def arquivo_path(self):
        return self._arquivo_path

    @arquivo_path.setter
    def arquivo_path(self, NovoArquivoPath):
        if not isinstance(NovoArquivoPath, str):
            raise ValueError("O caminho do arquivo deve ser uma string")
        NovoArquivoPath = NovoArquivoPath.strip()
        if NovoArquivoPath == "":
            raise ValueError("O caminho do arquivo não pode ser vazio")
        if len(NovoArquivoPath) < 3:
            raise ValueError("O caminho do arquivo deve ter pelo menos 3 caracteres")
        self._arquivo_path = NovoArquivoPath
    
    @property
    def ativo(self):
        return self._ativo

    @ativo.setter
    def ativo(self, NovoAtivo):
        if not isinstance(NovoAtivo, bool):
            raise ValueError("O status ativo deve ser um booleano")
        self._ativo = NovoAtivo