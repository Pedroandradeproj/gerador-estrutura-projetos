import os
import json
import tempfile
import zipfile
from flask import Flask, jsonify, request, send_file, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from src.backend.analyzer import StructureAnalyzer
from src.backend.generator import CodeGenerator

# Configurações do Flask
app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app)  # Permite requisições de diferentes origens
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'json'}

# Função para verificar arquivos permitidos
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Rota para upload e processamento de JSON
@app.route('/upload-json', methods=['POST'])
def upload_json():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Arquivo não encontrado na requisição'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Carregar o conteúdo do arquivo JSON
            with open(file_path, 'r') as f:
                estrutura = json.load(f)

            return jsonify({'mensagem': 'Estrutura recebida e processada com sucesso', 'estrutura': estrutura}), 200
        else:
            return jsonify({'error': 'Formato de arquivo inválido. Envie um arquivo JSON.'}), 400
    except Exception as e:
        return jsonify({'error': f'Ocorreu um erro ao processar o arquivo: {str(e)}'}), 500

# Rota para gerar estrutura de código a partir do JSON
@app.route("/gerar-estrutura", methods=["POST"])
def gerar_estrutura():
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

        # Gera o código
        codigo_gerado = generator.generate_code()
        return jsonify({"codigo": codigo_gerado})

    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

# Rota para baixar estrutura como .zip
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

        temp_dir = tempfile.mkdtemp()
        generator.create_structure()

        zip_path = os.path.join(temp_dir, "estrutura.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)

        return send_file(zip_path, as_attachment=True, download_name="estrutura.zip")
    except Exception as e:
        return jsonify({"erro": f"Erro ao gerar ou compactar a estrutura: {str(e)}"}), 500

# Rodando o servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
