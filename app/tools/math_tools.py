"""
Este módulo contém as ferramentas matemáticas.
"""

def calculate_operation(expression: str) -> str:
    """
    Avalia uma expressão matemática simples.

    Args:
        expression: A expressão matemática a ser calculada (ex: "1234 * 5678").

    Returns:
        O resultado da operação como string.
    """
    try:
        safe_expression = "".join(c for c in expression if c in "0123456789+-*/(). ")

        if not safe_expression:
            return "Erro: Expressão inválida."

        result = eval(safe_expression)
        return str(result)
    except Exception as e:
        return f"Erro ao calcular: {str(e)}"


if __name__ == "__main__":
    print(calculate_operation("10 * 5"))