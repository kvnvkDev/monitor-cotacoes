import io
import base64
import json
import os
from datetime import datetime

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
    ##Gera o gráfico com o historico da ação selecionada
    data = request.json
    valor = data['valor']

    y=[]
    x=[]
    for key, value in App.newData[valor].items():
          x.append(key)
          y.append(value["Adj Close"])
  
      #pega os ultivos 5 valores
    
    if len(x) < 10:
      x = x[-5:]
      y = y[-5:]
    elif len(x) > 10:# and len(x) < 25:
      x = x[::-5][:2]
      y = y[::-5][:2]
    """elif len(x) > 25:
      x = x[::-5][:5]
      y = y[::-5][:5]"""

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
      ##Gera o gráfico com dados do dia de cada ticker do usuário 
      arr = {}
      dt = datetime.today().strftime('%d-%m-%Y - %H:%M:%S')
      #print(datetime.today().strftime('%Y-%m-%d - %H:%M:%S'))
      print(App.dataFrame)
      if not App.dataFrame.empty:
            for key, value in App.dataFrame.groupby(level="Ticker"):
                  x = []
                  y = []
                  
                  # monta um dicionario com elementos de cada ticker para mostrar na tela principal [ultimo adj close, maior valor, menor valor, volume de negociação]
                  arr[key] = ["{:.2f}".format(value["Adj Close"].iloc[-1]), "{:.2f}".format(value["High"].max()), "{:.2f}".format(value["Low"].min()), value["Volume"].iloc[-1]]
                  for date, row in value.iterrows():
                        x.append(datetime.strftime(date[1], '%H:%M:%S'))
                        y.append(row["Adj Close"])
                  plt.figure()
                  plt.plot(x,y)
                  #Adicione os valores de y em cada ponto
                  for i, j in zip(x, y):
                        plt.text(i, j, f'{j:.2f}', ha='center', va='bottom')

                  plt.title(f'Gráfico para o valor {key}')
                  # Salvar o gráfico em um buffer
                  buf = io.BytesIO()
                  plt.savefig(buf, format='png')
                  buf.seek(0)
                  image_base64 = base64.b64encode(buf.read()).decode('utf-8')
                  buf.close()
                  #print(arr)

                  # adiciona a imagem em base64 no dicionário
                  arr[key].append(image_base64)

      return render_template('index.html', dados = arr, info = dt)

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


@web.route('/configuracoes', methods=['GET'])
def configuracoes():
      email = App.config['email']
      notificacao = App.config['notificacao']
      intervalo = App.config['intervalo']
      return render_template('configuracoes.html', conf = [email, notificacao, intervalo])


@web.route('/configuracoes', methods=['POST'])
def salvaConfiguracoes():
      #email = request.form['email']
      notif = request.form.get('notificacao')
      
      #App.config['email'] = email
      App.config['notificacao'] = True if notif == 'on' else False
      App.config['intervalo'] = request.form['intervalo']

      #atualiza arquivo config.json
      with open('config.json','w') as config:
                  json.dump(App.config,config)
                  print("Arquivo atualizado")
      return configuracoes()

@web.route('/historico', methods=['GET'])
def historico():
      return render_template('historico.html')

@web.route('/sobre', methods=['GET'])
def sobre():
      return render_template('sobre.html')

@web.route('/onOff', methods=['POST'])
def onOff():
      print("Fechando app")
      os._exit(0)
      return render_template('index.html')

if __name__ == '__main__':
      #app = App()
      web.run(threaded=True)
      print("run")
      
