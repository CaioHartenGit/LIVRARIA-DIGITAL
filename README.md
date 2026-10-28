# ✨ LuminaBooks — API de Biblioteca Digital, Mangás & Audiobook Studio

🌐 **Acesse a Plataforma Online (Netlify):** [https://luminabokks.netlify.app](https://luminabokks.netlify.app)  
⚙️ **API em Produção & Swagger UI (Render):** [https://luminabooks.onrender.com/docs](https://luminabooks.onrender.com/docs)

---

## 🎯 Propósito e Foco do Projeto (Back-end & Banco de Dados)

O **LuminaBooks** é um projeto desenvolvido com **foco principal em Engenharia de Software Back-end e Modelagem de Banco de Dados Relacional**.  

Todo o coração do sistema foi construído para praticar e consolidar conceitos essenciais de arquitetura de servidores:
* **Arquitetura em Camadas Estrita (`Entities` ➔ `Schemas` ➔ `Repository` ➔ `Service` ➔ `Routers`):** Separação total entre regras de domínio, validação de contratos (DTOs), persistência em SQL puro (`psycopg` sem depender de mágica de ORMs) e exposição de rotas HTTP REST com **FastAPI**.
* **Regras de Negócio e Controle de Acesso (RBAC & Multi-Tenancy por Usuário):** Isolamento de acervo por `usuario_id` (onde cada leitor vê apenas os livros que cadastrou, enquanto usuários `admin` possuem visão e gerenciamento global de todos os livros e contas do sistema).
* **Processamento de Arquivos e Otimização de Memória (`PyMuPDF` & `pypdf`):** Extração de texto para Audiobook e renderização sob demanda de páginas ilustradas/mangás em `JPEG Base64`, incluindo algoritmo de **fatiamento automático (`clip`)** para PDFs de tiras verticais gigantes (webtoons/mangás) rodando dentro do limite de 512 MB de RAM do servidor cloud.
* **Front-end Complementar:** A interface visual (`HTML5`, `CSS3` e `JavaScript`) foi implementada de forma prática e direta para servir como cliente real de consumo da API, permitindo testar visualmente os fluxos de upload, leitura e progresso.

---

## ☁️ Infraestrutura em Nuvem & Deploy (Cloud Stack)

| Camada | Plataforma | Função no Projeto |
| :--- | :--- | :--- |
| **Backend (API REST — Foco Principal)** | **Render** (`luminabooks.onrender.com`) | Servidor cloud rodando **FastAPI + Uvicorn + PyMuPDF** em produção |
| **Banco de Dados Relacional** | **Neon.tech** (Serverless PostgreSQL) | Banco PostgreSQL gerenciado na nuvem com chaves estrangeiras, `CASCADE` e `CHECK constraints` |
| **Front-end (Cliente Web)** | **Netlify** (`luminabokks.netlify.app`) | Interface web responsiva (Desktop & Mobile) consumindo a API REST |

---

## 🚀 Tecnologias Utilizadas

* **Back-end:** Python 3.14 + FastAPI + Uvicorn
* **Validação de Contratos (DTOs):** Pydantic v2 (`BaseModel`, `Field`, `ConfigDict`)
* **Banco de Dados & SQL:** PostgreSQL (`psycopg` v3 com `dict_row`) + **Neon Cloud Database**
* **Processamento de PDFs, Livros e Mangás:** `PyMuPDF` (`fitz`) + `pypdf` + `python-multipart`
* **Segurança & Configuração:** Variáveis de ambiente com `python-dotenv` (`.env` local e `DATABASE_URL` em produção)
* **Front-end & Audiobook:** HTML5, CSS3 Responsivo, JavaScript ES6+ e `Web Speech API` (narração TTS)

---

## 🏗️ Arquitetura do Back-end

O projeto segue uma **Arquitetura em Camadas (Layered Architecture)** rigorosa, garantindo que o arquivo `main.py` apenas inicialize a aplicação e que nenhuma rota (`Router`) execute SQL ou manipule arquivos diretamente:

```text
Cliente Web ──► Router (HTTP/FastAPI) ──► Service (Regras de Negócio/PDF) ──► Repository (SQL Puro) ──► PostgreSQL (Neon)
```

### Estrutura de Diretórios

```text
LuminaBooks/
├── main.py                              # Inicialização da API FastAPI, CORS, StaticFiles e registro de Routers
├── requirements.txt                     # Dependências enxutas de produção para o Render
├── netlify.toml                         # Configuração de publicação do diretório frontend
├── .env.example                         # Modelo público de variáveis de ambiente
├── .gitignore                           # Proteção de credenciais, cache e uploads locais
├── README.md                            # Documentação técnica do projeto
├── uploads/                             # Diretório de armazenamento dos PDFs enviados
├── apps/                                # NÚCLEO DO PROJETO (BACK-END EM CAMADAS)
│   ├── database/
│   │   └── conexao.py                   # Conexão híbrida PostgreSQL (Neon DATABASE_URL ou .env local)
│   ├── entities/
│   │   ├── livro.py                     # Entidade Livro com encapsulamento (@property/@setter) e usuario_id
│   │   ├── usuario.py                   # Entidade Usuario com validações de domínio e perfil (normal/admin)
│   │   └── progresso.py                 # Entidade Progresso com validações de páginas e status
│   ├── schemas/
│   │   ├── livro_schemas.py             # Contratos Pydantic (LivroCreate, LivroResponse)
│   │   ├── usuario_schemas.py           # Contratos Pydantic (UsuarioCreate, UsuarioLogin, UsuarioResponse)
│   │   └── progresso_schemas.py         # Contratos Pydantic (ProgressoCreate, ProgressoUpdate, ProgressoResponse)
│   ├── repository/
│   │   ├── livro_repository.py          # Queries SQL parametrizadas da tabela livro (filtro por dono e listagem admin)
│   │   ├── usuario_repository.py        # Queries SQL parametrizadas da tabela usuario
│   │   └── progresso_repository.py      # Queries SQL parametrizadas da tabela progresso
│   ├── services/
│   │   ├── livro_service.py             # Regras de negócio, RBAC de estante, extração de texto e fatiamento de Mangás
│   │   ├── usuario_service.py           # Regras de autenticação, cadastro e permissões de administrador
│   │   └── progresso_service.py         # Regras cruzadas entre Usuário, Livro e Progresso de leitura
│   └── routers/
│       ├── livro_routers.py             # Endpoints HTTP de livros, upload de PDF e leitura de páginas
│       ├── usuario_routers.py           # Endpoints HTTP de login, cadastro e gerenciamento de usuários
│       └── progresso_routers.py         # Endpoints HTTP de sincronização de progresso
└── frontend/                            # Interface Web complementar para consumo da API
    ├── index.html                       # Tela de Login e Cadastro
    ├── livros.html                      # Estante pessoal, estatísticas e modal de upload de PDF
    ├── leitor.html                      # Leitor Híbrido (Modo Texto Kindle + Modo Mangá/Imagem + Audiobook)
    ├── css/                             # Estilização modularizada e responsiva para smartphones
    └── js/                              # Integração via Fetch API com o Back-end no Render
```

---

## ⚙️ Principais Regras de Negócio Implementadas

### 1. 🔐 Isolamento de Acervo por Usuário vs. Visão de Administrador
* **Estante Privada (`tipo_usuario = 'normal'`):** Cada livro cadastrado recebe o `usuario_id` de quem fez o upload. Quando um usuário comum lista ou pesquisa livros (`GET /livros/?usuario_id={id}`), o `LivroService` retorna **exclusivamente** as obras cadastradas por ele.
* **Visão Global (`tipo_usuario = 'admin'`):** Quando o administrador consulta o acervo ou realiza buscas, o `LivroService` identifica a permissão `admin` no banco e retorna **todos os livros de todos os usuários**, além de liberar o painel de gerenciamento de contas (`GET /usuarios/admin/{id}`).

### 2. 🎌 Leitura Híbrida: Livros em Texto & Mangás / PDFs Ilustrados (`PyMuPDF`)
* **Extração Dupla sob Demanda (`GET /livros/{id}/pagina/{pagina}`):** A API extrai simultaneamente o texto selecionável da página (para leitura estilo Kindle e narração por voz) e renderiza a página original como imagem `JPEG Base64`.
* **Fatiamento Inteligente de Tiras Verticais (`obter_fatias_paginas`):** Capítulos de mangás ou webtoons exportados como uma única tira vertical gigante (ex: 1 página com `30.000px` de altura) são detectados automaticamente (`altura > largura * 2.2`) e fatiados virtualmente via `fitz.Rect` (`clip`), dividindo o capítulo em páginas individuais leves (~100 KB) sem sobrecarregar a memória RAM do servidor.

### 3. 📈 Controle de Progresso de Leitura (`ProgressoService`)
* Valida a existência do usuário e do livro antes de registrar o progresso.
* Impede que a `pagina_atual` ultrapasse o `total_paginas` real da obra.
* Marca automaticamente o atributo `concluido = True` assim que o leitor atinge a última página.

---

## 🗄️ Modelagem do Banco de Dados (PostgreSQL / Neon)

```sql
-- 1. Tabela de Usuários (com controle de perfil normal/admin)
CREATE TABLE IF NOT EXISTS usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(100) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    tipo_usuario VARCHAR(20) DEFAULT 'normal' CHECK (tipo_usuario IN ('normal', 'admin'))
);

-- 2. Tabela de Livros (vinculada ao usuário dono da obra)
CREATE TABLE IF NOT EXISTS livro (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    total_paginas INT NOT NULL CHECK (total_paginas > 0),
    arquivo_path VARCHAR(255) NOT NULL,
    usuario_id INT REFERENCES usuario(id) ON DELETE CASCADE,
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
| `POST` | `/livros/` | Recebe upload `.pdf`, fatia/calcula o total de páginas e vincula ao `usuario_id` |
| `GET` | `/livros/?usuario_id={id}` | Lista apenas os livros do usuário (ou todos os livros, se for `admin`) |
| `GET` | `/livros/{id}` | Busca os detalhes de um livro pelo ID |
| `GET` | `/livros/titulo/{titulo}?usuario_id={id}` | Pesquisa livros por título (`ILIKE`) respeitando a visibilidade do usuário |
| `GET` | `/livros/{id}/pagina/{pagina}` | Retorna o texto extraído e a imagem renderizada (`Base64`) da página ou fatia do mangá |
| `DELETE` | `/livros/{id}` | Remove um livro pelo ID |

### 👤 Usuários (`/usuarios`)
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `POST` | `/usuarios/login` | Autentica um usuário por e-mail e senha |
| `POST` | `/usuarios/` | Cadastra um novo usuário |
| `PUT` | `/usuarios/{id}` | Atualiza os dados de um usuário |
| `GET` | `/usuarios/admin/{id}` | Lista todos os usuários do sistema (exclusivo para `admin`) |
| `DELETE` | `/usuarios/{id_admin}?id_usuario={id}` | Remove um usuário do banco (exclusivo para `admin` ativo) |

### 📈 Progresso de Leitura (`/progresso`)
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `POST` | `/progresso/` | Inicia o registro de progresso de leitura de um livro para um usuário |
| `PUT` | `/progresso/{usuario_id}/{livro_id}/` | Atualiza a página atual de leitura e recalcula automaticamente se foi concluído |
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

4. **Acesse a documentação interativa:**
   * **Swagger UI Local:** `http://127.0.0.1:8000/docs`
   * **API em Produção (Render):** [https://luminabooks.onrender.com/docs](https://luminabooks.onrender.com/docs)
   * **Aplicação Web (Netlify):** [https://luminabokks.netlify.app](https://luminabokks.netlify.app)
