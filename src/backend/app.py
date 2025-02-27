import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS


# ✅ Garante que o diretório `src/` seja reconhecido pelo Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# ✅ Importa corretamente os módulos dentro de `backend/`
from src.backend.analyzer import StructureAnalyzer

from src.backend.generator import CodeGenerator

app = Flask(__name__)
CORS(app)  # Permite requisições de diferentes origens
@app.route("/")
def home():
    return jsonify({"mensagem": "API Gerador de Estrutura está funcionando!"})

@app.route("/gerar-estrutura", methods=["GET", "POST"])
def gerar_estrutura():
    if request.method == "GET":
        return jsonify({"mensagem": "Use um método POST para enviar a estrutura."})

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

if __name__ == "__main__":
    app.run(debug=True)
