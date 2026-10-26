class Usuario:
    def __init__(self,nome: str, email: str, senha: str,tipo_usuario: str, id: int = None, ativo: bool = True):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.tipo_usuario = tipo_usuario

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, novo_id: int):
        if novo_id is not None:
            if not isinstance(novo_id, int) or isinstance(novo_id, bool):
                raise ValueError("O ID do usuário deve ser um número inteiro")
            if novo_id <= 0:
                raise ValueError("O ID do usuário deve ser maior que 0")
        self._id = novo_id

    @property
    def nome(self):
        return self._nome
    @nome.setter
    def nome(self, novo_nome: str):
        if not isinstance(novo_nome,str):
            raise ValueError("O nome do usuário deve ser uma string")
        novo_nome = novo_nome.strip()
        if novo_nome == "":
            raise ValueError("O nome do usuário não pode ser vazio")
        if len(novo_nome) < 3:
            raise ValueError("O nome do usuário deve ter pelo menos 3 caracteres")
        self._nome = novo_nome

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, novo_email: str):
        if not isinstance(novo_email,str):
            raise ValueError("O email deve ser uma string")
        novo_email = novo_email.strip()
        if novo_email == "":
            raise ValueError("O email do usuário não pode ser vazio")
        if len(novo_email) < 3:
            raise ValueError("O email do usuário deve ter pelo menos 3 caracteres")
        if "@" not in novo_email or "." not in novo_email:
            raise ValueError("O email do usuário deve ser um email válido")
        if novo_email.count("@") != 1:
            raise ValueError("O email do usuário deve conter apenas um '@'")
        if novo_email.startswith("@") or novo_email.endswith("@"):
            raise ValueError("O email do usuário não pode começar ou terminar com '@'")
        if novo_email.startswith(".") or novo_email.endswith("."):
            raise ValueError("O email do usuário não pode começar ou terminar com '.'")
        self._email = novo_email

    @property
    def senha(self):
        return self._senha
    @senha.setter
    def senha(self, nova_senha: str):
        if not isinstance(nova_senha,str):
            raise ValueError("A senha deve ser uma string")
        nova_senha = nova_senha.strip()
        if nova_senha == "":
            raise ValueError("A senha do usuário não pode ser vazia")
        if len(nova_senha) < 3:
            raise ValueError("A senha do usuário deve ter pelo menos 3 caracteres")
        self._senha = nova_senha

    @property
    def ativo(self):
        return self._ativo
    @ativo.setter
    def ativo(self, novo_ativo: bool):
        if not isinstance(novo_ativo,bool):
            raise ValueError("O status de ativo deve ser um booleano")
        self._ativo = novo_ativo

    @property
    def tipo_usuario(self):
        return self._tipo_usuario
    @tipo_usuario.setter
    def tipo_usuario(self, novo_tipo_usuario: str):
        if not isinstance(novo_tipo_usuario,str):
            raise ValueError("O tipo de usuário deve ser uma string")
        novo_tipo_usuario = novo_tipo_usuario.strip()
        if novo_tipo_usuario == "":
            raise ValueError("O tipo de usuário não pode ser vazio")
        if len(novo_tipo_usuario) < 3:
            raise ValueError("O tipo de usuário deve ter pelo menos 3 caracteres")
        self._tipo_usuario = novo_tipo_usuario


            