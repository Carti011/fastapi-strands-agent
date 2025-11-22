from pydantic import BaseModel

class ChatRequest(BaseModel):
    """
    DTO para a requisição de chat.
    """
    message: str

class ChatResponse(BaseModel):
    """
    DTO para a resposta do chat.
    """
    response: str