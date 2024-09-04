
import json
import time
import traceback
from datetime import date,datetime
import os

import yfinance
from winotify import Notification
import pandas as pd

def timestamp_to_date(timestamp):
        return pd.to_datetime(timestamp, unit='ms')

class App:
    config = {}
    newData = {}
    dataFrame = pd.DataFrame()
    hj = date.today()
    sys = os.name
    def ini(self):
        on = True
        close = datetime(self.hj.year,self.hj.month,self.hj.day,18,00,0)

        #Carrega dados já existentes
        f = open('config.json')
        self.config = json.load(f)

        #Desativa notificação se false
        if not self.config['notificacao']:
            print(self.config['notificacao'])
            print(type(self.config['notificacao']))##
            App.sys = "none"

        with open('static/data.json') as fileData:
            file = fileData.read()
            if file.strip:
                self.newData = json.loads(file)
                print("Arquivo carregado")
            else:
                print("Arquivo vazio")
                
        #print(self.hj) 
        #print(self.config) 
        
        try:
            print("iniciando")
            if App.sys == "nt":
                alert = Notification(app_id="Gecko", title="O app está iniciando...",duration="short",launch="http://127.0.0.1:5000")
                alert.show()

            #Mantem o script em execução até as 18 horas
            while on:
                if (datetime.now() <= close):
                    self.atualiza(self.config, self.hj,(str(self.config["intervalo"])+'m'))
                    time.sleep(self.config["intervalo"]*60)
                else:
                    if App.sys == "nt":
                        alert = Notification(app_id="Gecko", title="O app está encerrando...", msg="A bolsa encerrou o dia 18h"+str(datetime.now),duration="short")
                    on = False
            if App.sys == "nt":
                alert.show()
        except Exception as e:
            print(traceback.format_exc())
            print("Erro: "+ str(e))
            if App.sys == "nt":
                alert = Notification(app_id="Gecko", title="O app foi encerrado com erro", msg="Erro: "+str(e),duration="long")
                alert.show()

    pass
    
    def atualiza(conf, dia, intervalo):
        dataF = {}
        #Baixa dados de cada ação e salva em data.json
        for i in conf["acoes"]:
            print(i)
            
            data = yfinance.download(i,period='1d', interval=intervalo)
            data.index = data.index.map(timestamp_to_date)

            
            if not data.empty:
                ##Construindo estrutura para salvar em data.json com dados extraidos do yfinance
                dailyData = {
                    "Adj Close": data["Adj Close"].iloc[-1],
                    "Open": data["Open"].iloc[0],
                    "High": data["High"].max(),
                    "Low" : data["Low"].min(),
                    "Close" : data["Close"].iloc[-1]
                    }

                # Adicionar o DataFrame ao dicionário usando o ticker como chave
                dataF[i] = data
            
                #Inclui novos dados no json com os dados existentes
                if i not in App.newData:
                    App.newData[i] = {dia.strftime('%Y-%m-%d'): dailyData}
                else:
                    if dia.strftime('%Y-%m-%d') not in App.newData[i]:
                        App.newData[i][dia.strftime('%Y-%m-%d')] = dailyData
                    else:
                        for key, value in dailyData.items():
                            App.newData[i][dia.strftime('%Y-%m-%d')][key] = value
        
                #Escreve novos dados no arquivo
                with open('static/data.json','w') as file:
                    json.dump(App.newData,file)
            # Concatenar os DataFrames do dicionário em um novo DataFrame
            App.dataFrame = pd.concat(dataF.values(), keys=dataF.keys(), names=['Ticker', 'Datetime'])
            #print(App.dataFrame)
        
        print("Atualizando dados...")
        if App.sys == "nt":
            alert = Notification(app_id="Gecko", title="Novas atualizações", duration="short", launch="http://127.0.0.1:5000")
            alert.show()
        pass

    #Verifica se ticker existe
    def tickerExiste(tick):
        r = yfinance.Ticker(tick).info
        if len(r) > 1:
            return True
        else:
            return False
        
    def t():
        while True:
            print("Teste iniciar app")
            time.sleep(60)