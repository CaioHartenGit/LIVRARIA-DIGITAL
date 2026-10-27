# ✨ LuminaBooks — Reading & Audiobook Studio

🌐 **Acesse a Plataforma Online (Netlify):** [https://luminabokks.netlify.app](https://luminabokks.netlify.app)  
⚙️ **API em Produção & Swagger UI (Render):** [https://luminabooks.onrender.com/docs](https://luminabooks.onrender.com/docs)

Plataforma Full-Stack de **Leitura Interativa Estilo Kindle e Audiobook Studio**, desenvolvida com **Python 3.14**, **FastAPI**, **Pydantic v2**, **PostgreSQL** e **pypdf** no Backend, interface modular em **HTML5, CSS3 (Glassmorphism) e JavaScript (Web Speech API)** no Front-end, e hospedada em nuvem utilizando **Netlify**, **Render** e **Neon Serverless Postgres**.

---

## ☁️ Infraestrutura em Nuvem & Deploy (Cloud Stack)

| Camada | Plataforma | Função no Projeto |
| :--- | :--- | :--- |
| **Front-end (Web App)** | **Netlify** (`luminabokks.netlify.app`) | Hospedagem global com CDN e deploy contínuo (CI/CD) via GitHub |
| **Backend (API REST)** | **Render** (`luminabooks.onrender.com`) | Servidor cloud rodando **FastAPI + Uvicorn** em produção |
| **Banco de Dados** | **Neon.tech** (Serverless PostgreSQL) | Banco de dados relacional PostgreSQL gerenciado na nuvem com SSL |

---

## 🚀 Tecnologias Utilizadas

* **Backend:** Python 3.14 + FastAPI + Uvicorn
* **Validação de Dados (DTOs):** Pydantic v2
* **Banco de Dados:** PostgreSQL (`psycopg` v3 com `dict_row`) + **Neon Cloud Database**
* **Segurança & Configuração:** Variáveis de ambiente com `python-dotenv` (`.env` / `.env.example` / `DATABASE_URL`)
* **Processamento de PDF:** `pypdf` (`PdfReader`) + `python-multipart`
* **Front-end & Audiobook:** HTML5, CSS3 Modular (`style-layout`, `style-components`, `style-pages`), JavaScript ES6+ e `Web Speech API` (TTS em Português)
* **Deploy & Cloud:** **Netlify** (Front-end), **Render** (Backend Web Service) e **Neon** (PostgreSQL Cloud)

---

## 🏗️ Arquitetura do Projeto

O projeto aplica **Arquitetura em Camadas (Layered / Clean Architecture)** no Backend integrada a um **Front-end Modular**:

```text
Front-end (Netlify) ──► Router (FastAPI / Render) ──► Service (Regras) ──► Repository (SQL) ──► PostgreSQL (Neon)
```

### Estrutura de Diretórios

```text
LuminaBooks/
├── main.py                              # Ponto de entrada da API FastAPI + CORS + StaticFiles
├── requirements.txt                     # Dependências de produção para o Render
├── netlify.toml                         # Configuração de publicação automática na Netlify
├── .env                                 # Variáveis de ambiente locais (ignorado pelo Git)
├── .env.example                         # Modelo público de variáveis de ambiente
├── .gitignore                           # Proteção de credenciais, cache e uploads locais
├── README.md                            # Documentação completa do projeto
├── uploads/                             # Diretório onde os PDFs enviados são armazenados
├── frontend/                            # Interface Visual LuminaBooks & Audiobook Studio
│   ├── index.html                       # Tela Split-Screen de Login e Cadastro
│   ├── livros.html                      # Dashboard de Estatísticas, Estante 3D e Upload de PDF
│   ├── leitor.html                      # Leitor Estilo Kindle (Noturno/Sépia/Claro) + LuminaVox Player
│   ├── css/
│   │   ├── style-layout.css             # Variáveis globais, tipografia, Navbar, Containers e Grids
│   │   ├── style-components.css         # Botões, Inputs, Cards 3D, Barra de Progresso e Modais
│   │   └── style-pages.css              # Estilos específicos de cada tela, temas Kindle e equalizador
│   └── js/
│       ├── auth.js                      # Autenticação e sessão do usuário
│       ├── livros.js                    # Catálogo, filtros, estatísticas e envio de PDF
│       └── leitor.js                    # Leitura de páginas, sincronização de progresso e voz TTS
└── apps/
    ├── database/
    │   └── conexao.py                   # Conexão híbrida (Neon DATABASE_URL ou .env local)
    ├── entities/
    │   ├── livro.py                     # Entidade Livro com encapsulamento (@property/@setter)
    │   ├── usuario.py                   # Entidade Usuario com validações de domínio
    │   └── progresso.py                 # Entidade Progresso com validações de tipos e datas
    ├── schemas/
    │   ├── livro_schemas.py             # Schemas Pydantic (LivroCreate, LivroResponse)
    │   ├── usuario_schemas.py           # Schemas Pydantic (UsuarioCreate, UsuarioLogin, UsuarioResponse)
    │   └── progresso_schemas.py         # Schemas Pydantic (ProgressoCreate, ProgressoUpdate, ProgressoResponse)
    ├── repository/
    │   ├── livro_repository.py          # Queries SQL da tabela livro
    │   ├── usuario_repository.py        # Queries SQL da tabela usuario
    │   └── progresso_repository.py      # Queries SQL da tabela progresso
    ├── services/
    │   ├── livro_service.py             # Regras de negócio de livros e extração de páginas com pypdf
    │   ├── usuario_service.py           # Regras de negócio de usuários, login e permissões RBAC
    │   └── progresso_service.py         # Regras cruzadas entre Usuário, Livro e Progresso
    └── routers/
        ├── livro_routers.py             # Rotas HTTP de livros, upload de PDF e leitura de página
        ├── usuario_routers.py           # Rotas HTTP de login, cadastro e administração
        └── progresso_routers.py         # Rotas HTTP de progresso de leitura
```

---

## ⚙️ Funcionalidades Completas

### 1. 🎨 Interface LuminaBooks & LuminaVox Audiobook Studio
* **Tela Split-Screen de Autenticação (`index.html`):** Vitrine interativa da plataforma e acesso rápido de Login/Cadastro.
* **Dashboard de Estatísticas & Estante 3D (`livros.html`):** Exibe contadores em tempo real (*Obras no Acervo*, *Em Leitura*, *Livros Concluídos* e *Total de Páginas Lidas*), filtros por status (*Todos*, *Lendo Agora*, *Concluídos*) e capas estilizadas.
* **Leitor Estilo Kindle (`leitor.html`):** Alternância entre temas **🌙 Noturno**, **📜 Sépia** e **☀️ Claro**, escolha de tipografia (**Livro Serif** ou **Moderna Sans**), controle de tamanho da fonte (`A-` / `A+`) e navegação pelas setas do teclado (`⬅️` / `➡️`).
* **Player de Audiobook com Auto-Avanço:** Narra o texto extraído do PDF em Português com equalizador animado, controle de velocidade (`0.9x` a `1.5x`) e opção de virar a página automaticamente ao terminar a narração.

### 2. 📖 Módulo de Livros & Upload Real de PDF (`pypdf`)
* **Upload Real de PDF (`UploadFile`):** Envio do arquivo `.pdf` pela interface para todos os usuários (`normal` e `admin`).
* **Contagem Automática de Páginas:** O `PdfReader` calcula automaticamente o `total_paginas` do PDF no momento do upload.
* **Extração de Página sob Demanda:** A rota `GET /livros/{id}/pagina/{pagina}` extrai o texto exato da folha solicitada.

### 3. 👤 Módulo de Usuários, Login & RBAC
* **Perfis de Acesso (`normal` e `admin`):** Qualquer usuário autenticado pode publicar PDFs e ler livros; administradores possuem acesso exclusivo ao **Painel de Usuários (`GET /usuarios/admin/{id}`)** para listar e gerenciar todas as contas cadastradas.
* **Proteção de Dados:** O `UsuarioResponse` nunca expõe a senha nos retornos JSON.

### 4. 📈 Módulo de Progresso de Leitura
* **Sincronização Automática:** Cada virada de página no leitor atualiza automaticamente a `pagina_atual` no PostgreSQL (Neon).
* **Conclusão Inteligente:** Ao alcançar a última página do livro (`pagina_atual == total_paginas`), o livro é marcado automaticamente como `concluido = True`.

---

## 🗄️ Modelagem do Banco de Dados (PostgreSQL / Neon)

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
| `POST` | `/usuarios/login` | Autentica um usuário por e-mail e senha |
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

## ▶️ Como Executar Localmente

1. **Instale as dependências:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Configure as variáveis de ambiente (`.env`):**
   Crie um arquivo `.env` na raiz do projeto com base no `.env.example` (ou informe a `DATABASE_URL` do **Neon**):
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

4. **Acesse a aplicação:**
   * **Produção (Netlify):** [https://luminabokks.netlify.app](https://luminabokks.netlify.app)
   * **API Swagger (Render):** [https://luminabooks.onrender.com/docs](https://luminabooks.onrender.com/docs)
