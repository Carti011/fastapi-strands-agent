from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """
    Modelo de dados para a requisição de entrada do chat.
    """
    message: str = Field(..., description="A mensagem de texto enviada pelo usuário.", min_length=1)

class ChatResponse(BaseModel):
    """
    Modelo de dados para a resposta do Agente.
    """
    response: str = Field(..., description="A resposta textual gerada pelo Agente de IA.")