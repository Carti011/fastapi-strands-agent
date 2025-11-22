import os
import requests
from dotenv import load_dotenv
from app.tools.math_tools import calculate_operation

load_dotenv()

try:
    from strands_agents import Agent, Tool

    print("SUCESSO: strands_agents carregado oficialmente.")
except ImportError:
    print("AVISO: strands_agents não encontrado. Usando MOCKS INTELIGENTES para rodar localmente.")

    class Tool:
        """
        Stub da classe Tool para quando a lib oficial não existe.
        """

        def __init__(self, name, description, func):
            self.name = name
            self.description = description
            self.func = func


    class Agent:
        """
        Stub da classe Agent que simula o comportamento chamando o Ollama via HTTP.
        """

        def __init__(self, model, base_url, tools, system_prompt):
            self.model = model
            self.base_url = base_url
            self.tools = tools
            self.system_prompt = system_prompt

        def run(self, message: str) -> str:
            """
            Simula a execução do agente.
            Se detectar necessidade de cálculo, usa a tool diretamente.
            Caso contrário, chama o Ollama via request HTTP padrão.
            """
            # Se a mensagem tiver números e operadores, tentamos calcular
            if any(op in message for op in ['+', '*', '-', '/']) and any(char.isdigit() for char in message):
                print(f"[MOCK AGENT] Detectei uma operação matemática. Usando tool: calculator")
                # Pega a tool de calculadora
                result = self.tools[0].func(message)
                return f"Usei a ferramenta de cálculo. O resultado é: {result}"

            # Se não for cálculo, chama o Ollama diretamente via API REST
            try:
                payload = {
                    "model": self.model,
                    "prompt": f"{self.system_prompt}\nUser: {message}\nAssistant:",
                    "stream": False
                }
                response = requests.post(f"{self.base_url}/api/generate", json=payload)

                if response.status_code == 200:
                    data = response.json()
                    return data.get("response", "Erro: O Ollama não retornou texto.")
                else:
                    return f"Erro no Ollama (Status {response.status_code}): {response.text}"
            except Exception as e:
                return f"Erro de conexão com Ollama: {str(e)}"


class AIService:
    """
    Service responsável por gerenciar o Agente de IA.
    """

    def __init__(self):
        self.model_name = os.getenv("OLLAMA_MODEL", "llama3:latest")
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        self.math_tool = Tool(
            name="calculator",
            description="Útil para realizar cálculos matemáticos.",
            func=calculate_operation
        )

        self.agent = Agent(
            model=self.model_name,
            base_url=self.base_url,
            tools=[self.math_tool],
            system_prompt="Você é um assistente útil. Se o usuário pedir um cálculo, eu mesmo resolverei."
        )

    def get_response(self, user_message: str) -> str:
        try:
            response = self.agent.run(user_message)
            return str(response)
        except Exception as e:
            return f"Erro ao processar mensagem: {str(e)}"


ai_service = AIService()