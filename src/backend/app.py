from flask import Flask, request, jsonify, send_file, send_from_directory
import tempfile
import zipfile
import os
from src.backend.analyzer import StructureAnalyzer
from src.backend.generator import CodeGenerator

app = Flask(__name__, static_folder="../frontend", static_url_path="/")

# Rota para gerar estrutura de projeto
@app.route("/gerar-estrutura", methods=["POST"])
def gerar_estrutura():
    if request.method == "GET":
        return jsonify({"erro": "Método GET não é permitido. Use POST."}), 405

    if request.content_type != "application/json":
        return jsonify({"erro": "O cabeçalho Content-Type deve ser application/json"}), 415

    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"erro": "O corpo da requisição está vazio ou inválido"}), 400

        input_text = data.get("estrutura", "")
        if not input_text:
            return jsonify({"erro": "O campo 'estrutura' é obrigatório"}), 400

        analyzer = StructureAnalyzer(input_text)
        estrutura = analyzer.get_structure()

        generator = CodeGenerator(estrutura)
        codigo_gerado = generator.generate_code()

        return jsonify({"codigo": codigo_gerado})

    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

# Rota para baixar estrutura gerada como um arquivo .zip
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
    generator.create_structure(base_path=temp_dir)  # Usando o método create_structure

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

# Iniciar servidor no modo produção
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
