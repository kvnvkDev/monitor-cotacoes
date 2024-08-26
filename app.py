
import json
import time
import traceback
from random import randint
from datetime import date,datetime


import yfinance
from winotify import Notification

class App:
    def ini(self):
        on = True
        hj = date.today()
        close = datetime(hj.year,hj.month,hj.day,18,00,0)#18
        f = open('config.json')
        config = json.load(f)

        print(hj) 
        
        try:
            print("iniciando")
            alert = Notification(app_id="Gecko", title="O app está iniciando...",duration="short")
            alert.show()

            #Mantem o script em execução até as 18 horas
            while on:
                if (datetime.now() <= close):
                    self.teste(config, hj,(str(config["intervalo"])+'m'))
                    time.sleep(config["intervalo"]*60)
                else:
                    alert = Notification(app_id="Gecko", title="O app está encerrando...", msg="A bolsa encerrou o dia 18h"+str(datetime.now),duration="short")
                    on = False
    
            alert.show()
        except Exception as e:
            print(traceback.format_exc())
            print("Erro: "+ str(e))
            alert = Notification(app_id="Gecko", title="O app foi encerrado com erro", msg="Erro: "+str(e),duration="long")
            alert.show()

    pass
    
    def teste(conf, dia, intervalo):
        print(str(conf["intervalo"])+'m')
    
        #Baixa dados de cada ação e salva em data.json
        for i in conf["acoes"]:
            print(i)
            data = yfinance.download(i,period='1d', interval=intervalo)
            dataJson = data.to_json()
            print(dataJson)
       
            ##Construindo estrutura para salvar em data.json com dados extraidos do yfinance
            dailyData = {
                "Adj Close": data["Adj Close"].iloc[-1],
                "Open": data["Open"].iloc[0],
                "High": data["High"].max(),
                "Low" : data["Low"].min(),
                "Close" : data["Close"].iloc[-1]
                }

            #Carrega dados já existentes da ação
            with open('static/data.json') as fileData:
                file = fileData.read()
                if file.strip:
                    newData = json.loads(file)
                    print("Arquivo carregado")
                else:
                    print("Arquivo vazio")
                    newData = {}
        
            #Inclui novos dados no json com os dados existentes
            if i not in newData:
                newData[i] = {dia.strftime('%Y-%m-%d'): dailyData}
            else:
                if dia.strftime('%Y-%m-%d') not in newData[i]:
                    newData[i][dia.strftime('%Y-%m-%d')] = dailyData
                else:
                    for key, value in dailyData.items():
                        newData[i][dia.strftime('%Y-%m-%d')][key] = value
        
            #Escreve novos dados no arquivo
            with open('static/data.json','w') as file:
                json.dump(newData,file)

        print("Atualizando dados...")
        alert = Notification(app_id="Gecko", title="Novas atualizações", duration="short", launch="")
        alert.show()
        pass

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