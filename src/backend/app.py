import os
import zipfile
import tempfile
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Função que simula a análise da estrutura (ajuste conforme necessário)
class StructureAnalyzer:
    def __init__(self, input_text):
        self.input_text = input_text

    def get_structure(self):
        # Lógica para analisar a estrutura do input_text
        # Aqui, estamos simulando uma estrutura simples.
        return [
            {"type": "folder", "name": "folder1"},
            {"type": "folder", "name": "folder2"},
            {"type": "file", "name": "folder1/file1.txt", "content": "Conteúdo do arquivo 1"},
            {"type": "file", "name": "folder2/file2.txt", "content": "Conteúdo do arquivo 2"}
        ]

# Função para gerar a estrutura de pastas e arquivos (ajuste conforme necessário)
class CodeGenerator:
    def __init__(self, structure):
        self.structure = structure

    def create_structure(self, base_path):
        for item in self.structure:
            if item["type"] == "folder":
                folder_path = os.path.join(base_path, item["name"])
                os.makedirs(folder_path, exist_ok=True)
            elif item["type"] == "file":
                file_path = os.path.join(base_path, item["name"])
                with open(file_path, 'w') as file:
                    file.write(item["content"])

# Função para adicionar arquivos ao .zip e garantir que as pastas sejam criadas
def add_file_to_zip(zipf, file_path, arcname):
    """
    Função para adicionar um arquivo ao zip, criando os diretórios necessários.
    """
    # Cria os diretórios no zip se não existirem
    dir_name = os.path.dirname(arcname)
    if dir_name:
        zipf.write(file_path, arcname)  # Cria o diretório no zip antes de adicionar o arquivo

# Rota para baixar estrutura gerada como um arquivo .zip
@app.route("/baixar-estrutura", methods=["POST"])
def baixar_estrutura():
    if not request.is_json:
        return jsonify({"erro": "O corpo da requisição deve ser JSON"}), 415

    data = request.get_json()
    input_text = data.get("estrutura", "")

    if not input_text:
        return jsonify({"erro": "O campo 'estrutura' é obrigatório"}), 400

    try:
        # Analisa e gera a estrutura
        analyzer = StructureAnalyzer(input_text)
        estrutura = analyzer.get_structure()
        generator = CodeGenerator(estrutura)

        # Cria a estrutura em um diretório temporário
        temp_dir = tempfile.mkdtemp()
        generator.create_structure(temp_dir)  # Gera a estrutura de arquivos e pastas

        # Compacta a estrutura
        zip_path = os.path.join(temp_dir, "estrutura.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    add_file_to_zip(zipf, file_path, arcname)  # Adiciona os arquivos ao .zip com a estrutura correta

        # Envia o arquivo .zip para o cliente
        return send_file(zip_path, as_attachment=True, download_name="estrutura.zip")

    except Exception as e:
        return jsonify({"erro": f"Erro ao gerar ou compactar a estrutura: {str(e)}"}), 500

# Inicia o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
