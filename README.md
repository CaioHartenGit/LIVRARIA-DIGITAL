# 📚 Livraria Digital API

API RESTful completa para gerenciamento de uma **Biblioteca e Livraria Digital**, desenvolvida com **Python 3.14**, **FastAPI**, **Pydantic v2**, **PostgreSQL** e **pypdf**.

O sistema permite o cadastro de usuários com controle de acesso (**RBAC**), upload real de livros em formato **PDF** (com contagem automática de páginas), extração inteligente do texto página a página (preparado para leitura e **Audiobook**) e acompanhamento completo do **Progresso de Leitura** de cada usuário.

---

## 🚀 Tecnologias Utilizadas

* **Linguagem:** Python 3.14
* **Framework Web:** FastAPI + Uvicorn
* **Validação de Dados (DTOs):** Pydantic v2
* **Banco de Dados:** PostgreSQL (`psycopg` v3 com `dict_row`)
* **Segurança & Configuração:** Variáveis de ambiente com `python-dotenv` (`.env` / `.env.example`)
* **Processamento de PDF & Audiobook:** `pypdf` (`PdfReader`) + `python-multipart`

---

## 🏗️ Arquitetura do Projeto

O projeto foi construído aplicando **Arquitetura em Camadas (Layered / Clean Architecture)**, garantindo separação clara de responsabilidades e tratamento centralizado de regras de negócio:

```text
Router (FastAPI) ──► Service (Regras de Negócio) ──► Repository (SQL / PostgreSQL) ──► Entity (Domínio)
```

### Estrutura de Diretórios

```text
LIVRARIA_DIGITAL/
├── main.py                              # Ponto de entrada da aplicação FastAPI
├── .env                                 # Variáveis de ambiente locais (ignorado pelo Git)
├── .env.example                         # Modelo de variáveis de ambiente para configuração
├── .gitignore                           # Proteção de credenciais, cache e arquivos locais
├── README.md                            # Documentação do projeto
├── uploads/                             # Diretório onde os PDFs enviados são armazenados
└── apps/
    ├── database/
    │   └── conexao.py                   # Conexão segura com o PostgreSQL via variáveis de ambiente
    ├── entities/
    │   ├── livro.py                     # Entidade Livro com encapsulamento (@property/@setter)
    │   ├── usuario.py                   # Entidade Usuario com validações de domínio
    │   └── progresso.py                 # Entidade Progresso com validações de tipos e datas
    ├── schemas/
    │   ├── livro_schemas.py             # Schemas Pydantic (LivroCreate, LivroResponse)
    │   ├── usuario_schemas.py           # Schemas Pydantic (UsuarioCreate, UsuarioResponse)
    │   └── progresso_schemas.py         # Schemas Pydantic (ProgressoCreate, ProgressoUpdate, ProgressoResponse)
    ├── repository/
    │   ├── livro_repository.py          # Queries SQL da tabela livro
    │   ├── usuario_repository.py        # Queries SQL da tabela usuario
    │   └── progresso_repository.py      # Queries SQL da tabela progresso
    ├── services/
    │   ├── livro_service.py             # Regras de negócio de livros e leitura de páginas com pypdf
    │   ├── usuario_service.py           # Regras de negócio de usuários e permissões RBAC
    │   └── progresso_service.py         # Regras cruzadas entre Usuário, Livro e Progresso
    └── routers/
        ├── livro_routers.py             # Rotas HTTP de livros, upload de PDF e leitura de página
        ├── usuario_routers.py           # Rotas HTTP de usuários e administração
        └── progresso_routers.py         # Rotas HTTP de progresso de leitura
```

---

## ⚙️ Funcionalidades Implementadas

### 1. 📖 Módulo de Livros, Upload Real de PDF & Audiobook
* **Upload Real de PDF (`UploadFile`):** Ao cadastrar um livro, o usuário envia o arquivo `.pdf` diretamente pelo formulário da API. O arquivo é salvo automaticamente na pasta `uploads/`.
* **Contagem Automática de Páginas (`pypdf`):** O sistema abre o PDF enviado utilizando o `PdfReader` e calcula automaticamente o `total_paginas` antes de gravar no banco de dados.
* **Leitura de Página para Audiobook:** Rota dedicada que extrai o texto exato de qualquer página do livro (`leitor.pages[pagina - 1].extract_text()`), permitindo exibir o texto na tela e alimentar a leitura em voz alta (**Audiobook**).

### 2. 👤 Módulo de Usuários & Controle de Acesso (RBAC)
* **Perfis de Acesso (`normal` e `admin`):** Diferenciação entre leitores comuns e administradores diretamente no banco de dados.
* **Segurança de Dados (DTO):** O `UsuarioResponse` omite a senha em todos os retornos da API.
* **Rotas Exclusivas para Admin:** Listagem geral de usuários e exclusão de contas validam se o solicitante possui `tipo_usuario == 'admin'` e está ativo.

### 3. 📈 Módulo de Progresso de Leitura
* **Relacionamento Único (`Usuário x Livro`):** Cada usuário possui um registro único de progresso por livro (`UNIQUE (usuario_id, livro_id)`).
* **Validação Cruzada (*Fail-Fast*):** O `ProgressoService` consulta `UsuarioRepository`, `LivroRepository` e `ProgressoRepository` para garantir que usuário e livro existem antes de registrar ou atualizar a leitura.
* **Trava de Limite de Páginas:** Impede que o usuário informe uma `pagina_atual` maior que o `total_paginas` real do livro.
* **Conclusão Automática:** Quando `pagina_atual == total_paginas`, o sistema define automaticamente `concluido = True` (e reverte para `False` caso o leitor volte para uma página anterior).

---

## 🗄️ Modelagem do Banco de Dados (PostgreSQL)

```sql
-- 1. Tabela de Livros
CREATE TABLE IF NOT EXISTS livro (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    total_paginas INT NOT NULL CHECK (total_paginas > 0),
    arquivo_path VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabela de Usuários (com RBAC)
CREATE TABLE IF NOT EXISTS usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(100) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    tipo_usuario VARCHAR(20) DEFAULT 'normal' CHECK (tipo_usuario IN ('normal', 'admin'))
);

-- 3. Tabela de Progresso de Leitura
CREATE TABLE IF NOT EXISTS progresso (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    livro_id INT NOT NULL,
    pagina_atual INT DEFAULT 0 NOT NULL CHECK (pagina_atual >= 0),
    concluido BOOLEAN DEFAULT FALSE,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_usuario FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE,
    CONSTRAINT fk_livro FOREIGN KEY (livro_id) REFERENCES livro(id) ON DELETE CASCADE,
    CONSTRAINT uq_usuario_livro UNIQUE (usuario_id, livro_id)
);
```

---

## 🛣️ Rotas da API (Endpoints)

### 📚 Livros (`/livros`)
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `POST` | `/livros/` | Faz upload de um arquivo `.pdf`, calcula o total de páginas e cadastra o livro |
| `GET` | `/livros/` | Lista todos os livros cadastrados |
| `GET` | `/livros/{id}` | Busca os detalhes de um livro pelo ID |
| `GET` | `/livros/titulo/{titulo}` | Busca livros por parte do título (`ILIKE`) |
| `GET` | `/livros/{id}/pagina/{pagina}` | Extrai o texto de uma página específica do PDF (Leitura / Audiobook) |
| `DELETE` | `/livros/{id}` | Remove um livro pelo ID |

### 👤 Usuários (`/usuarios`)
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `POST` | `/usuarios/` | Cadastra um novo usuário |
| `PUT` | `/usuarios/{id}` | Atualiza os dados de um usuário |
| `GET` | `/usuarios/admin/{id}` | Lista todos os usuários (exclusivo para administradores) |
| `DELETE` | `/usuarios/{id_admin}?id_usuario={id}` | Deleta um usuário (exclusivo para administradores ativos) |

### 📈 Progresso de Leitura (`/progresso`)
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `POST` | `/progresso/` | Inicia o registro de progresso de leitura de um livro para um usuário |
| `PUT` | `/progresso/{usuario_id}/{livro_id}/` | Atualiza a página atual de leitura e recalcula o status de conclusão |
| `GET` | `/progresso/{usuario_id}/` | Lista todo o histórico de leitura de um usuário |
| `DELETE` | `/progresso/{id}/` | Remove um registro de progresso pelo ID |

---

## ▶️ Como Executar o Projeto

1. **Instale as dependências:**
   ```bash
   pip3 install fastapi uvicorn "psycopg[binary]" pypdf python-multipart python-dotenv
   ```

2. **Configure as variáveis de ambiente (`.env`):**
   Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:
   ```env
   DB_NAME=LIVRARIA-DIGITAL
   DB_USER=postgres
   DB_PASSWORD=sua_senha_aqui
   DB_HOST=localhost
   DB_PORT=5432
   ```

3. **Inicie o servidor FastAPI:**
   ```bash
   uvicorn main:app --reload
   ```

4. **Acesse a documentação interativa (Swagger UI):**
   👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
