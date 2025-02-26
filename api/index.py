from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime

app = Flask(__name__)

@app.route('/comprovant', methods=['GET'])
def comprovant():
    nome = request.args.get('nome')
    if not nome:
        return {'error': 'Nome não fornecido'}, 400

    # Caminho correto dos arquivos
    image_path = "api/comprovante_template.png"
    font_path = "api/arialbd.ttf"

    # Carregar imagem
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        return {'error': 'Imagem não encontrada'}, 500

    # Configurar desenho
    draw = ImageDraw.Draw(image)

    # Carregar fonte personalizada
    try:
        font_nome = ImageFont.truetype(font_path, 40)
    except IOError:
        font_nome = ImageFont.load_default()

    # Adicionar texto na imagem
    text_position = (28, 185)
    draw.text(text_position, nome, font=font_nome, fill="black")

    # Adicionar data atual
    data_atual = datetime.now().strftime("%d/%m/%Y")
    data_position = (220, 280)
    draw.text(data_position, data_atual, font=font_nome, fill="black")

    # Adicionar data de vencimento
    vencimento_position = (700, 280)
    draw.text(vencimento_position, data_atual, font=font_nome, fill="white")

    # Salvar imagem em memória e retornar
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

# Expor a aplicação para Vercel
def handler(event, context):
    return app(event, context)
if isinstance(base, type) and issubclass(base, BaseHTTPRequestHandler):
