from pathlib import Path

class CodeGenerator:
    def __init__(self, structure):
        self.structure = structure

    def generate_code(self):
        """
        Gera o código Python para criar a estrutura de pastas e arquivos corretamente aninhada.
        """
        code_lines = ["from pathlib import Path", ""]

        # Obtém a pasta raiz do projeto a partir da primeira linha da estrutura
        base_folder = self.structure[0]["path"].strip("/")
        code_lines.append(f"base_path = Path.cwd() / '{base_folder}'")

        # Garante que a pasta principal só seja criada uma vez
        code_lines.append("if not base_path.exists():")
        code_lines.append("    base_path.mkdir(parents=True, exist_ok=True)")

        created_dirs = {base_folder}  # Mantém controle das pastas já criadas

        for item in self.structure[1:]:  # Ignora a primeira linha, pois já criamos a raiz
            relative_path = item["path"].replace(f"{base_folder}/", "", 1).lstrip("/")
            path = f'Path(base_path / "{relative_path}")'  # ✅ Garante que `Path()` seja aplicado corretamente

            if item["type"] == "folder":
                if relative_path not in created_dirs:
                    code_lines.append(f'if not {path}.exists():')
                    code_lines.append(f'    {path}.mkdir(parents=True, exist_ok=True)')
                    created_dirs.add(relative_path)
            elif item["type"] == "file":
                # Garante que a pasta pai do arquivo exista antes de criá-lo
                parent_folder = "/".join(relative_path.split("/")[:-1])
                if parent_folder and parent_folder not in created_dirs:
                    parent_path = f'Path(base_path / "{parent_folder}")'
                    code_lines.append(f'if not {parent_path}.exists():')
                    code_lines.append(f'    {parent_path}.mkdir(parents=True, exist_ok=True)')
                    created_dirs.add(parent_folder)
                code_lines.append(f'if not {path}.exists():')
                code_lines.append(f'    {path}.touch()')

        code_lines.append('\nprint(f"Estrutura criada com sucesso em: {base_path}")')
        return "\n".join(code_lines)

    def create_structure(self):
        """
        Cria a estrutura de pastas e arquivos diretamente no sistema de arquivos.
        """
        # Obtém a pasta raiz do projeto a partir da primeira linha da estrutura
        base_folder = self.structure[0]["path"].strip("/")
        base_path = Path.cwd() / base_folder

        # Criação da pasta principal
        if not base_path.exists():
            base_path.mkdir(parents=True, exist_ok=True)

        created_dirs = {base_folder}  # Mantém controle das pastas já criadas

        for item in self.structure[1:]:
            relative_path = item["path"].replace(f"{base_folder}/", "", 1).lstrip("/")
            path = base_path / relative_path

            if item["type"] == "folder":
                if relative_path not in created_dirs:
                    path.mkdir(parents=True, exist_ok=True)
                    created_dirs.add(relative_path)
            elif item["type"] == "file":
                # Garante que a pasta pai do arquivo exista antes de criá-lo
                parent_folder = "/".join(relative_path.split("/")[:-1])
                if parent_folder and parent_folder not in created_dirs:
                    parent_path = base_path / parent_folder
                    parent_path.mkdir(parents=True, exist_ok=True)
                    created_dirs.add(parent_folder)
                path.touch()

        print(f"Estrutura criada com sucesso em: {base_path}")