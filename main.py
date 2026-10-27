from fastapi import FastAPI
from apps.routers.livro_routers import router as livro_router
from apps.routers.usuario_routers import router as usuario_router
from apps.routers.progresso_routers import router as progresso_router

app = FastAPI(title="Biblioteca Digital API")

# Inclui as rotas do livro
app.include_router(livro_router)
app.include_router(usuario_router)
app.include_router(progresso_router)
