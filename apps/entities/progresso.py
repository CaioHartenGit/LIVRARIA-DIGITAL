from datetime import datetime

class Progresso:
    def __init__(self, usuario_id: int, livro_id: int, pagina_atual = 0, concluido = False, id = None, atualizado_em = None):
        self.usuario_id = usuario_id
        self.livro_id = livro_id
        self.pagina_atual = pagina_atual
        self.concluido = concluido
        self.id = id
        self.atualizado_em = atualizado_em

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, NovoId: int):
        if NovoId is not None:
            if not isinstance(NovoId, int) or isinstance (NovoId, bool):
                raise ValueError("O ID do progresso deve ser um número inteiro")
            if NovoId<=0:
                raise ValueError("O ID do progresso deve ser maior que zero")
        self._id = NovoId

    @property
    def usuario_id(self):
        return self._usuario_id
    @usuario_id.setter
    def usuario_id(self, NovoUsuarioId: int):
        if not isinstance(NovoUsuarioId, int) or isinstance (NovoUsuarioId, bool):
            raise ValueError("O usuário do progresso deve ser um número inteiro")
        if NovoUsuarioId<=0:
            raise ValueError("O usuário do progresso deve ser maior que zero")
        self._usuario_id = NovoUsuarioId

    @property
    def livro_id(self):
        return self._livro_id
    @livro_id.setter
    def livro_id(self, NovoLivroId: int):
        if not isinstance(NovoLivroId, int) or isinstance (NovoLivroId, bool):
            raise ValueError("O livro do progresso deve ser um número inteiro")
        if NovoLivroId<=0:
            raise ValueError("O livro do progresso deve ser maior que zero")
        self._livro_id = NovoLivroId
    
    @property
    def pagina_atual(self):
        return self._pagina_atual
    @pagina_atual.setter
    def pagina_atual(self, NovaPaginaAtual: int):
        if not isinstance(NovaPaginaAtual, int) or isinstance (NovaPaginaAtual, bool):
            raise ValueError("A página atual do progresso deve ser um número inteiro")
        if NovaPaginaAtual<0:
            raise ValueError("A página atual do progresso não pode ser negativa")
        self._pagina_atual = NovaPaginaAtual
    
    @property
    def concluido(  self):
        return self._concluido
    @concluido.setter
    def concluido(self, NovoConcluido: bool):
        if not isinstance(NovoConcluido, bool):
            raise ValueError("O concluído do progresso deve ser um booleano")
        self._concluido = NovoConcluido
    
    @property
    def atualizado_em(self):
        return self._atualizado_em
    @atualizado_em.setter
    def atualizado_em(self, NovoAtualizadoEm: datetime):
        if NovoAtualizadoEm is not  None:
            if not isinstance(NovoAtualizadoEm, datetime):
                raise ValueError("O atualizado em do progresso deve ser um datetime")
        self._atualizado_em = NovoAtualizadoEm
    
    

