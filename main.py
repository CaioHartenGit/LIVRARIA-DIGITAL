import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from apps.routers.livro_routers import router as livro_router
from apps.routers.usuario_routers import router as usuario_router
from apps.routers.progresso_routers import router as progresso_router

app = FastAPI(title="Biblioteca Digital API")

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
