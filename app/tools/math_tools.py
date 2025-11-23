"""
Módulo responsável pelas ferramentas matemáticas do Agente.
"""

def calculate_operation(expression: str) -> str:
    """
    Avalia uma expressão matemática simples de forma segura.

    Realiza a sanitização da string de entrada para permitir apenas
    números e operadores básicos, prevenindo execução de código arbitrário.

    Args:
        expression (str): A expressão matemática (ex: "1234 * 5678").

    Returns:
        str: O resultado da operação ou uma mensagem de erro.
    """
    try:
        # Sanitização: Remove qualquer caracter que não seja dígito ou operador básico.
        # Em produção, considerar o uso de bibliotecas como 'numexpr' ou 'ast.literal_eval'
        # para maior segurança e performance em expressões complexas.
        safe_expression = "".join(c for c in expression if c in "0123456789+-*/(). ")

        if not safe_expression:
            return "Erro: Expressão vazia ou caracteres inválidos detectados."

        # O uso de eval aqui é controlado pela sanitização acima.
        result = eval(safe_expression)
        return str(result)

    except SyntaxError:
        return "Erro: Sintaxe matemática incorreta."
    except ZeroDivisionError:
        return "Erro: Divisão por zero não permitida."
    except Exception as e:
        return f"Erro desconhecido ao processar cálculo: {str(e)}"

if __name__ == "__main__":
    # Teste local rápido da função
    print(calculate_operation("10 * 5"))