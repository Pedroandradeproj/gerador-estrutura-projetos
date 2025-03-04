# Responsável por validar a entrada do usuário
import re

class InputValidator:
    @staticmethod
    def validate(input_text):
        """
        Valida a entrada do usuário e retorna uma lista de erros (se houver).
        """
        errors = []
        # Verifica caracteres inválidos
        invalid_chars = re.findall(r"[*?:<>|]", input_text)
        if invalid_chars:
            errors.append(f"Caracteres inválidos encontrados: {set(invalid_chars)}")
        # Verifica se há pelo menos uma pasta/arquivo
        if not any("/" in line or "\\" in line for line in input_text.splitlines()):
            errors.append("Nenhuma pasta ou arquivo válido encontrado.")
        return errors