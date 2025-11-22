import os
from dotenv import load_dotenv

from app.tools.math_tools import calculate_operation

try:
    from strands_agents import Agent, Tool
except ImportError:
    print("AVISO: strands_agents não encontrado. Usando mocks para estruturar o código.")

    class Agent:
        pass

    class Tool:
        pass

load_dotenv()


class AIService:
    """
    Service responsável por gerenciar o Agente de IA.
    """

    def __init__(self):
        # Configuração inicial
        self.model_name = os.getenv("OLLAMA_MODEL", "llama3:latest")
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        # Registrar a Tool
        self.math_tool = Tool(
            name="calculator",
            description="Útil para realizar cálculos matemáticos. Entrada deve ser uma expressão matemática simples ex: '2 + 2'.",
            func=calculate_operation
        )

        # Inicializar o Agente
        self.agent = Agent(
            model=self.model_name,
            base_url=self.base_url,
            tools=[self.math_tool],
            system_prompt="Você é um assistente útil. Se o usuário pedir um cálculo, USE a ferramenta 'calculator'. Não tente calcular de cabeça."
        )

    def get_response(self, user_message: str) -> str:
        """
        Metodo principal que recebe a mensagem do usuário e retorna a resposta da IA.
        """
        try:
            response = self.agent.run(user_message)
            return str(response)
        except Exception as e:
            return f"Erro ao processar mensagem: {str(e)}"


ai_service = AIService()