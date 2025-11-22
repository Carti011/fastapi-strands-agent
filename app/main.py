from fastapi import FastAPI
import uvicorn
from app.api.routes import router

# Inicializa a aplicação
app = FastAPI(
    title="Strands AI Agent API",
    description="API de Chat com Agente Inteligente e Tools Matemáticas",
    version="1.0.0"
)

# Registra as rotas
app.include_router(router)

# Endpoint de verificação de saude
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "running"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)