from apps.schemas.usuario_schemas import UsuarioCreate, UsuarioLogin

class UsuarioService:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def login(self, email, senha):
        login_data = UsuarioLogin(email=email, senha=senha)
        usuario = self.usuario_repository.buscar_por_email_com_senha(login_data.email)
        if not usuario:
            raise ValueError("Email ou senha inválidos")
        if not usuario["ativo"]:
            raise ValueError("Usuário inativo no sistema")
        if usuario["senha"] != login_data.senha:
            raise ValueError("Email ou senha inválidos")

        return {
            "id": usuario["id"],
            "nome": usuario["nome"],
            "email": usuario["email"],
            "ativo": usuario["ativo"],
            "tipo_usuario": usuario["tipo_usuario"]
        }

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

    def deletar_usuario(self, id_usuario, id_admin):
        administrador = self.usuario_repository.buscar_usuario_por_id(id_admin)

        if administrador is None:
            raise ValueError("Administrador não encontrado")
        if administrador["tipo_usuario"] != "admin" or not administrador["ativo"]:
            raise PermissionError("Apenas administradores ativos podem deletar usuários")

        usuario = self.usuario_repository.buscar_usuario_por_id(id_usuario)
        if usuario is None:
            raise ValueError("Usuário a ser deletado não encontrado")

        self.usuario_repository.deletar_usuario(id_usuario)
