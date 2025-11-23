from fastapi import APIRouter, HTTPException
from app.api.schemas import ChatRequest, ChatResponse
from app.agents.core_agent import ai_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse, summary="Enviar mensagem para o Agente")
async def chat_endpoint(request: ChatRequest):
    """
    Processa uma mensagem do usuário através do Agente de IA.

    O fluxo identifica automaticamente se é necessária a utilização de
    ferramentas (Tools) ou se é uma resposta de conhecimento geral (LLM pura).
    """
    try:
        agent_response = ai_service.get_response(request.message)
        return ChatResponse(response=agent_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha interna no processamento do Agente: {str(e)}")