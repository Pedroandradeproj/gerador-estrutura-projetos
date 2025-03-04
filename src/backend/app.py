import sys
import os
import tempfile
import zipfile
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS

# ✅ Garante que o diretório `src/` seja reconhecido pelo Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# ✅ Importa corretamente os módulos dentro de `backend/`
from src.backend.analyzer import StructureAnalyzer
from src.backend.generator import CodeGenerator

app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app)  # Permite requisições de diferentes origens

# 🔹 Servir o frontend (HTML) ao acessar "/"
@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

# 🔹 Servir arquivos estáticos (CSS, JS, imagens)
@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

# 🔹 Rota para gerar estrutura de projeto
@app.route("/gerar-estrutura", methods=["POST"])
def gerar_estrutura():
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

# 🔹 Rota para baixar estrutura gerada como um arquivo .zip
@app.route("/baixar-estrutura", methods=["POST"])
def baixar_estrutura():
    if not request.is_json:
        return jsonify({"erro": "O corpo da requisição deve ser JSON"}), 415

    data = request.get_json()
    input_text = data.get("estrutura", "")

    if not input_text:
        return jsonify({"erro": "O campo 'estrutura' é obrigatório"}), 400

    try:
        analyzer = StructureAnalyzer(input_text)
        estrutura = analyzer.get_structure()
        generator = CodeGenerator(estrutura)

        # Criar diretório temporário
        temp_dir = tempfile.mkdtemp()
        output_dir = os.path.join(temp_dir, "projeto")
        os.makedirs(output_dir, exist_ok=True)

        # Gerar a estrutura dentro do diretório correto
        generator.create_structure(output_dir)

        # Compactar estrutura gerada
        zip_path = os.path.join(temp_dir, "estrutura.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, output_dir)
                    zipf.write(file_path, arcname)

        return send_file(zip_path, as_attachment=True, download_name="estrutura.zip")

    except Exception as e:
        return jsonify({"erro": f"Erro ao gerar ou compactar a estrutura: {str(e)}"}), 500

# 🔹 Iniciar servidor no modo produção
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
