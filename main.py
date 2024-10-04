import os
import cups
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Isso permite CORS para todas as rotas e origens


# Configura a conexão com o servidor CUPS
conn = cups.Connection()

# Pasta onde os arquivos enviados serão salvos temporariamente
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configuração do Flask para a pasta de uploads
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/print', methods=['POST'])
def print_file():
    # Verifica se o arquivo foi enviado na requisição
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo foi enviado"}), 400

    file = request.files['file']

    # Se nenhum arquivo for selecionado
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    # Salvar o arquivo no servidor
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Pega a lista de impressoras disponíveis
    printers = conn.getPrinters()
    print(list(printers))
    default_printer = list(printers.keys())[0]  # Pega a primeira impressora como exemplo

    # Envia o arquivo para a impressora padrão
    try:
        conn.printFile(default_printer, file_path, "Python Print Job", {})
        return jsonify({"message": f"Arquivo '{file.filename}' enviado para a impressora '{default_printer}'."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
