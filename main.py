import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from apps.database.conexao import Conectar
from apps.routers.livro_routers import router as livro_router
from apps.routers.usuario_routers import router as usuario_router
from apps.routers.progresso_routers import router as progresso_router

app = FastAPI(title="Biblioteca Digital API")


@app.on_event("startup")
def garantir_coluna_usuario_id_livro():
    try:
        conn = Conectar.conectar()
        cursor = conn.cursor()
        cursor.execute(
            '''
            ALTER TABLE livro
            ADD COLUMN IF NOT EXISTS usuario_id INTEGER REFERENCES usuario(id) ON DELETE CASCADE;

            UPDATE livro
            SET usuario_id = (SELECT id FROM usuario WHERE tipo_usuario = 'admin' ORDER BY id ASC LIMIT 1)
            WHERE usuario_id IS NULL;
            '''
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as erro:
        print(f"Aviso na migração automática da tabela livro: {erro}")

# Habilitando CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servindo arquivos estáticos de upload
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Inclui as rotas do livro
app.include_router(livro_router)
app.include_router(usuario_router)
app.include_router(progresso_router)
