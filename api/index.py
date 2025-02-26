from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime

app = Flask(__name__)

@app.route('/comprovant', methods=['GET'])
def comprovant():
    nome = request.args.get('nome')  # Pega o parâmetro 'nome' da URL
    if not nome:
        return {'error': 'Nome não fornecido'}, 400

    # Carrega a imagem (deixe o arquivo "comprovante_template.png" na raiz do projeto)
    image = Image.open("comprovante_template.png")

    # Configuração para escrever o nome na imagem
    draw = ImageDraw.Draw(image)

    # Carregar uma fonte personalizada para o nome
    try:
        font_nome = ImageFont.truetype("arialbd.ttf", 40)  # Arial negrito
    except IOError:
        font_nome = ImageFont.load_default()

    # Definir a posição do texto
    text_position = (28, 185)
    draw.text(text_position, nome, font=font_nome, fill="black")

    # Adiciona a data atual
    data_atual = datetime.now().strftime("%d/%m/%Y")
    data_position = (220, 280)
    draw.text(data_position, data_atual, font=font_nome, fill="black")

    # Adiciona a data de vencimento
    vencimento_position = (700, 280)
    draw.text(vencimento_position, data_atual, font=font_nome, fill="white")

    # Salva a imagem modificada em um buffer de memória
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

def handler(event, context):
    return app(event, context)
