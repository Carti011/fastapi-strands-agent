import os
import requests
from dotenv import load_dotenv
from app.tools.math_tools import calculate_operation

load_dotenv()

# Tentativa de importação do SDK oficial 'strands_agents'.
# Caso a biblioteca não esteja disponível no ambiente (ex: PyPI privado),
# o sistema utiliza classes Stub (Mock) para garantir a execução local e testes.
try:
    from strands_agents import Agent, Tool
    print("INFO: SDK 'strands_agents' carregado com sucesso.")
except ImportError:
    print("WARN: SDK 'strands_agents' não detectado. Utilizando implementação Mock para desenvolvimento local.")

    class Tool:
        """
        Representação Mock da classe Tool do SDK Strands.
        Permite o registro de funções locais como ferramentas do agente.
        """
        def __init__(self, name, description, func):
            self.name = name
            self.description = description
            self.func = func

    class Agent:
        """
        Representação Mock da classe Agent.
        Simula a orquestração entre LLM (via Ollama API) e Tools locais.
        """
        def __init__(self, model, base_url, tools, system_prompt):
            self.model = model
            self.base_url = base_url
            self.tools = tools
            self.system_prompt = system_prompt

        def run(self, message: str) -> str:
            """
            Executa o pipeline do agente:
            1. Analisa a intenção (Heurística simples para o Mock).
            2. Executa a Tool se necessário.
            3. Ou chama o LLM via API REST padrão se for conversação geral.
            """
            # Heurística simples para simular a decisão do modelo de usar a calculadora
            if any(op in message for op in ['+', '*', '-', '/']) and any(char.isdigit() for char in message):
                # Simulação de chamada de Tool (Function Calling)
                tool_result = self.tools[0].func(message)
                return f"Realizei o cálculo solicitado. Resultado: {tool_result}"

            # Fallback para conversação direta com o Ollama
            try:
                payload = {
                    "model": self.model,
                    "prompt": f"{self.system_prompt}\nUser: {message}\nAssistant:",
                    "stream": False
                }
                response = requests.post(f"{self.base_url}/api/generate", json=payload)

                if response.status_code == 200:
                    data = response.json()
                    return data.get("response", "Erro: Resposta vazia do modelo.")
                else:
                    return f"Erro na comunicação com LLM (Status {response.status_code})"
            except Exception as e:
                return f"Erro de conexão com o serviço de LLM: {str(e)}"


class AIService:
    """
    Service Layer responsável pela inicialização e ciclo de vida do Agente de IA.
    Implementa o padrão Singleton implicitamente ao instanciar o objeto no módulo.
    """

    def __init__(self):
        # Configurações via variáveis de ambiente
        self.model_name = os.getenv("OLLAMA_MODEL", "llama3:latest")
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        # Registro de Ferramentas
        self.math_tool = Tool(
            name="calculator",
            description="Realiza cálculos matemáticos precisos. Entrada: string da expressão.",
            func=calculate_operation
        )

        # Configuração do Agente
        self.agent = Agent(
            model=self.model_name,
            base_url=self.base_url,
            tools=[self.math_tool],
            system_prompt="Você é um assistente inteligente capaz de realizar cálculos e responder perguntas gerais."
        )

    def get_response(self, user_message: str) -> str:
        """Encapsula a chamada ao agente, tratando erros de execução."""
        try:
            return str(self.agent.run(user_message))
        except Exception as e:
            # Em produção, adicionar logs estruturados aqui
            return f"Desculpe, encontrei um erro interno: {str(e)}"

# Instância única exportada para uso nos controladores
ai_service = AIService()