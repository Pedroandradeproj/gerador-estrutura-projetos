import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# ✅ Garante que o diretório `src/` seja reconhecido pelo Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# ✅ Importa corretamente os módulos dentro de `backend/`
from backend.analyzer import StructureAnalyzer
from backend.generator import CodeGenerator

app = Flask(__name__)
CORS(app)  # Permite requisições de diferentes origens (necessário para o frontend acessar o backend)

@app.route("/gerar-estrutura", methods=["POST"])
def gerar_estrutura():
    if not request.is_json:
        return jsonify({"erro": "O corpo da requisição deve ser JSON"}), 415

    data = request.get_json()  # Obtém os dados JSON do request
    input_text = data.get("estrutura", "")

    # Processa a estrutura usando os módulos do backend
    analyzer = StructureAnalyzer(input_text)
    estrutura = analyzer.get_structure()

    generator = CodeGenerator(estrutura)
    codigo_gerado = generator.generate_code()

    return jsonify({"codigo": codigo_gerado})

if __name__ == "__main__":
    app.run(debug=True)
