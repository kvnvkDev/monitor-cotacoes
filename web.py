import io
import base64
import json


from flask import Flask, request, jsonify, render_template
import matplotlib.pyplot as plt

from app import *



with open('static/data.json') as fileData:
            file = fileData.read()
            if file.strip:
                newData = json.loads(file)
                print("Arquivo carregado")



web = Flask(__name__)

@web.route('/executar_script', methods=['POST'])
def executar_script():
    
    data = request.json
    valor = data['valor']

    ##Gera o gráfico com o historico da ação selecionada
    y=[]
    x=[]
    for key, value in newData[valor].items():
          #x.insert(0,key)
          x.append(key)
          y.append(value["Adj Close"])
  

    plt.figure()
    plt.plot(x,y)
    plt.title(f'Gráfico para o valor {valor}')

    # Salvar o gráfico em um buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return jsonify({'image': image_base64})

@web.route('/', methods=['GET'])
def index():
      return render_template('index.html')

@web.route('/historico', methods=['GET'])
def historico():
      return render_template('historico.html')

@web.route('/onOff', methods=['POST'])#testar
def onOff():
      app.on = False
      return render_template('index.html')

if __name__ == '__main__':
    web.run(debug=True)
    app = App()