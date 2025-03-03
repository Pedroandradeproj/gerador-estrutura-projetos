from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import tempfile
import zipfile
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Permite requisições de diferentes origens

@app.route("/gerar-estrutura", methods=["POST"])
def gerar_estrutura():
    if not request.is_json:
        return jsonify({"erro": "O corpo da requisição deve ser JSON"}), 415

    data = request.get_json()
    input_text = data.get("estrutura", "")

    # Processa a estrutura usando os módulos do backend
    analyzer = StructureAnalyzer(input_text)
    estrutura = analyzer.get_structure()

    generator = CodeGenerator(estrutura)
    codigo_gerado = generator.generate_code()

    return jsonify({"codigo": codigo_gerado})

@app.route("/baixar-estrutura", methods=["POST"])
def baixar_estrutura():
    if not request.is_json:
        return jsonify({"erro": "O corpo da requisição deve ser JSON"}), 415

    data = request.get_json()
    input_text = data.get("estrutura", "")

    # Analisa e gera a estrutura
    analyzer = StructureAnalyzer(input_text)
    estrutura = analyzer.get_structure()
    generator = CodeGenerator(estrutura)

    # Cria a estrutura em um diretório temporário
    temp_dir = tempfile.mkdtemp()
    generator.create_structure(base_path=temp_dir)

    # Compacta a estrutura
    zip_path = os.path.join(temp_dir, "estrutura.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)

    # Envia o arquivo .zip para o cliente
    return send_file(zip_path, as_attachment=True, download_name="estrutura.zip")

if __name__ == "__main__":
    app.run(debug=True)