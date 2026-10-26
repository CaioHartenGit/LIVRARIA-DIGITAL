from apps.schemas.usuario_schemas import UsuarioCreate

class UsuarioService:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def cadastrar(self, nome, email, senha):
        usuariocriar = UsuarioCreate(nome = nome, email = email, senha = senha)
        
        usuariocadastrado = self.usuario_repository.buscar_por_email(usuariocriar.email)
        if usuariocadastrado:
            raise ValueError("Já existe um usuário com esse email cadastrado")

        return self.usuario_repository.cadastrar(
            usuariocriar.nome,
            usuariocriar.email,
            usuariocriar.senha,
        )

    def atualiza_usuario(self, nome, email, senha, id):
        usuario_atualizado = self.usuario_repository.atualizar_usuario( nome, email, senha, id)
        if not usuario_atualizado:
            raise ValueError("Usuário não encontrado")
        return usuario_atualizado

    def listar_tudo_admin(self,id):
        usuario = self.usuario_repository.buscar_usuario_por_id(id)
        if usuario is None:
            raise ValueError("Usuário não encontrado")
        if usuario['tipo_usuario'] != 'admin':
            raise ValueError("Acesso negado. Apenas administradores podem listar todos os usuários.")
        return self.usuario_repository.listar_tudo_admin()