from apps.schemas.progresso_schemas import ProgressoCreate, ProgressoUpdate


class ProgressoService:
    def __init__(self, progresso_repository, usuario_repository, livro_repository):
        self.progresso_repository = progresso_repository
        self.usuario_repository = usuario_repository
        self.livro_repository = livro_repository

    def cadastrar_progresso(self, usuario_id, livro_id, pagina_atual):
        progressoCRIAR = ProgressoCreate(
            usuario_id=usuario_id,
            livro_id=livro_id,
            pagina_atual=pagina_atual
        )

        usuarioExiste = self.usuario_repository.buscar_usuario_por_id(progressoCRIAR.usuario_id)
        if not usuarioExiste:
            raise ValueError("Usuário não encontrado")

        livroExiste = self.livro_repository.buscar_livro_por_id(progressoCRIAR.livro_id)
        if not livroExiste:
            raise ValueError("Livro não encontrado")

        usuarioJaEstaLendo = self.progresso_repository.buscar_por_usuario_e_livro(
            progressoCRIAR.usuario_id,
            progressoCRIAR.livro_id
        )
        if usuarioJaEstaLendo:
            raise ValueError("Usuário já está lendo esse livro")

        if pagina_atual > livroExiste["total_paginas"]:
            raise ValueError("A página atual não pode ultrapassar o total de páginas do livro")

        if pagina_atual == livroExiste["total_paginas"]:
            progressoCRIAR.concluido = True
        else:
            progressoCRIAR.concluido = False

        return self.progresso_repository.cadastrar_progresso(
            progressoCRIAR.usuario_id,
            progressoCRIAR.livro_id,
            progressoCRIAR.pagina_atual,
            progressoCRIAR.concluido
        )

    def atualizar_pagina(self, usuario_id, livro_id, pagina_atual):
        progressoAtualizado = ProgressoUpdate(pagina_atual=pagina_atual)

        progressoExiste = self.progresso_repository.buscar_por_usuario_e_livro(usuario_id, livro_id)
        if progressoExiste is None:
            raise ValueError("Progresso não encontrado para este usuário e livro")

        limite_pagina = self.livro_repository.buscar_livro_por_id(livro_id)
        if limite_pagina is None:
            raise ValueError("Livro não encontrado")

        if pagina_atual > limite_pagina["total_paginas"]:
            raise ValueError("A página atual não pode ultrapassar o total de páginas do livro")

        if pagina_atual == limite_pagina["total_paginas"]:
            concluido = True
        else:
            concluido = False

        return self.progresso_repository.atualizar_pagina(
            usuario_id,
            livro_id,
            progressoAtualizado.pagina_atual,
            concluido
        )

    def listar_por_usuario(self, usuario_id):
        usuarioExiste = self.usuario_repository.buscar_usuario_por_id(usuario_id)
        if not usuarioExiste:
            raise ValueError("Usuário não encontrado")

        lista_progresso = self.progresso_repository.listar_por_usuario(usuario_id)
        if not lista_progresso:
            raise ValueError("Progresso não encontrado para este usuário")

        return lista_progresso

    def deletar_progresso(self, id):
        delete = self.progresso_repository.deletar_progresso(id)
        if delete is None:
            raise ValueError("Progresso não encontrado para ser deletado")
        return delete

    
 