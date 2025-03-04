import re

class StructureAnalyzer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.cleaned_lines = self._clean_input()
        self.root_folder = None  # Armazena a raiz do projeto

    def _clean_input(self):
        """
        Remove comentários e linhas vazias da entrada do usuário.
        """
        cleaned_lines = []
        for line in self.input_text.splitlines():
            # Remove comentários (tudo após #)
            line = re.sub(r"#.*", "", line).rstrip()
            if line:  # Ignora linhas vazias
                cleaned_lines.append(line)
        return cleaned_lines

    def get_structure(self):
        """
        Retorna a estrutura de pastas/arquivos corretamente aninhada.
        """
        structure = []
        stack = []  # Mantém o histórico de diretórios para criar caminhos corretos

        for index, line in enumerate(self.cleaned_lines):
            # Conta a indentação real (incluindo caracteres gráficos como espaço)
            indent_level = len(line) - len(line.lstrip(" │├└─"))  # Contando os caracteres gráficos

            # Remove caracteres gráficos, mas mantém o alinhamento correto
            clean_line = re.sub(r"[│├└──]+", "", line).strip()

            # Define a raiz do projeto na primeira linha
            if index == 0:
                self.root_folder = clean_line.rstrip("/")  # Remove barra final se houver
                stack = [(indent_level, self.root_folder)]
                structure.append({"type": "folder", "path": self.root_folder})
                continue

            # Define corretamente a hierarquia com base na indentação
            while stack and stack[-1][0] >= indent_level:
                stack.pop()  # Remove diretórios de níveis superiores

            parent_path = stack[-1][1] if stack else self.root_folder
            full_path = f"{parent_path}/{clean_line}".replace("//", "/").rstrip("/")

            # Detecta se é um **arquivo** ou uma **pasta** corretamente
            if clean_line.endswith("/") or "." not in clean_line:  # Se termina com / ou **não tem extensão**, é pasta
                stack.append((indent_level, full_path))
                structure.append({"type": "folder", "path": full_path})
            else:  # Se tem extensão, é um arquivo
                structure.append({"type": "file", "path": full_path})

        return structure
