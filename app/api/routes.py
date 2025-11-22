from fastapi import APIRouter, HTTPException
from app.api.schemas import ChatRequest, ChatResponse
from app.agents.core_agent import ai_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint para conversar com o Agente.
    Recebe um JSON com 'message' e retorna 'response'.
    """
    try:
        agent_response = ai_service.get_response(request.message)
        return ChatResponse(response=agent_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))