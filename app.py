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

    # Carrega a imagem (substitua pelo caminho da sua imagem)
    image = Image.open("comprovante_template.png")

    # Configuração para escrever o nome na imagem
    draw = ImageDraw.Draw(image)

    # Carregar uma fonte personalizada para o nome (ajuste o caminho para a sua fonte)
    try:
        # Usar uma fonte TTF ou OTF (como Arial ou outra fonte em negrito)
        font_nome = ImageFont.truetype("arialbd.ttf", 40)  # Arial em negrito, tamanho 40
    except IOError:
        # Se a fonte não for encontrada, usa a fonte padrão
        print("Fonte não encontrada, usando a fonte padrão.")
        font_nome = ImageFont.load_default()

    # Definir a posição do texto (ajuste conforme necessário)
    text_position = (28, 185)

    # Desenha o nome na imagem
    draw.text(text_position, nome, font=font_nome, fill="black")

    # Carregar uma fonte personalizada para a data (ajuste o caminho para a sua fonte)
    try:
        font_data = ImageFont.truetype("arialbd.ttf", 20)  # Fonte menor para as datas
    except IOError:
        font_data = ImageFont.load_default()

    # Adiciona a data atual (de hoje) na posição desejada
    data_atual = datetime.now().strftime("%d/%m/%Y")
    data_position = (220, 280)
    draw.text(data_position, data_atual, font=font_data, fill="black")

    # Adiciona a data de vencimento (mesmo dia)
    vencimento_position = (700, 280)
    draw.text(vencimento_position, data_atual, font=font_data, fill="white")

    # Salva a imagem em um objeto de bytes para enviar como resposta
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)

    # Retorna a imagem com o nome, data e vencimento adicionados
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
