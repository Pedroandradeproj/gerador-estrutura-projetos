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

# 🔹 Rota inicial para exibir um link para o frontend
@app.route("/")
def home():
    frontend_url = "https://gerador-estrutura-projetos-nrk2.onrender.com/gerar-estrutura"  # 🔹 Substitua pelo link real do frontend
    return f"""
    <html>
        <head>
            <title>API Gerador de Estrutura</title>
        </head>
        <body style="text-align: center; font-family: Arial, sans-serif;">
            <h1>🚀 API Gerador de Estrutura</h1>
            <p>Acesse o frontend clicando no botão abaixo:</p>
            <a href="{frontend_url}" style="display: inline-block; padding: 10px 20px; font-size: 16px; color: white; background-color: #007BFF; text-decoration: none; border-radius: 5px;">
                Ir para o Frontend
            </a>
        </body>
    </html>
    """

# 🔹 Rota para gerar estrutura de projeto
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

# 🔹 Iniciar servidor no modo produção
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
