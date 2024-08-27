import io
import base64
import json

import os

from flask import Flask, request, jsonify, render_template
import matplotlib.pyplot as plt

from app import *



"""with open('static/data.json') as fileData:
      file = fileData.read()
      if file.strip:
            newData = json.loads(file)
            print("Arquivo carregado")

with open('config.json') as fileConfig:
            config = fileConfig.read()
            conf = json.loads(config)"""


web = Flask(__name__)

@web.route('/gerarGrafico', methods=['POST'])
def gerarGrafico():
    
    data = request.json
    valor = data['valor']

    ##Gera o gráfico com o historico da ação selecionada
    y=[]
    x=[]
    for key, value in App.newData[valor].items():
          #x.insert(0,key)
          x.append(key)
          y.append(value["Adj Close"])
  
      #pega os ultivos 5 valores
    x = x[-5:]
    y = y[-5:]

      # Pegando os valores  de 5 em 5
      #x = x[::-5][:5]
      #y = y[::-5][:5]

    plt.figure()
    plt.plot(x,y)

    #Adicione os valores de y em cada ponto
    for i, j in zip(x, y):
      plt.text(i, j, f'{j:.2f}', ha='center', va='bottom')

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

@web.route('/listaAcoes', methods=['GET'])
def listaAcoes():
      listaTicker = App.config["acoes"]
      return render_template('listaAcoes.html', status = "", tickers = listaTicker)

@web.route('/deleteAcoes/<string:ticker>', methods=['POST'])
def deleteAcoes(ticker):
      print(ticker)
            
      App.config["acoes"].remove(ticker)
      listaTicker = App.config["acoes"]

      #atualiza arquivo config.json
      with open('config.json','w') as config:
            json.dump(App.config,config)
            print("Arquivo atualizado")
      return render_template('listaAcoes.html',status = "" ,tickers = listaTicker)

@web.route('/addAcoes', methods=['POST'])
def addAcoes():
      ticker = request.form['ticker']
      listaTicker = App.config["acoes"]

      if App.tickerExiste(ticker):
            App.config["acoes"].append(ticker)
            #print(conf)
            #App.config = conf
            listaTicker = App.config["acoes"]
            #atualiza arquivo config.json
            with open('config.json','w') as config:
                  json.dump(App.config,config)
                  print("Arquivo atualizado")
            retorno = "Ticker " + ticker + " adicionado."
            return render_template('listaAcoes.html',status = retorno, tickers=listaTicker)
      else:
            retorno = "&#9888 O ticker " + ticker + " não existe. Verifique o código no Yahoo Finance."
            print(retorno)
            return render_template('listaAcoes.html',status = retorno, tickers=listaTicker)


@web.route('/historico', methods=['GET'])
def historico():
      return render_template('historico.html')


@web.route('/onOff', methods=['POST'])
def onOff():
      print("Fechando app")
      os._exit(0)
      return render_template('index.html')

if __name__ == '__main__':
      #app = App()
      web.run(threaded=True)
      print("run")
      
      