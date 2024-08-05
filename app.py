
import json
import time
import traceback
from random import randint
from datetime import date,datetime


import yfinance
from winotify import Notification

class App:

    

   

    def __init__(self):
        on = True
        hj = date.today()
        close = datetime(hj.year,hj.month,hj.day,12,30,0)#18
        f = open('config.json')
        config = json.load(f)

        print(hj) 
        
        try:
            print("iniciando")
            alert = Notification(app_id="Gecko", title="O app está iniciando...",duration="short")
            alert.show()
            print(type(close))
            print(type(datetime.now()))
            while on:
                if (datetime.now() <= close):
                    self.teste()
                    time.sleep(30*60)#(config["intervalo"]*60)
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
    
    def teste(self):
        print(str(self.config["intervalo"])+'m')
    
        for i in self.config["acoes"]:
            print(i)
            data = yfinance.download(i,period='1d', interval=('30m'))#str(config["intervalo"])+'m'
            dataJson = data.to_json()
            print(dataJson)
        ##ff = open("ndata.json",'w')
        ##ff.write(dataJson)
        ##ff.close()
        ##Coonstruindo estrutura para salvar em data.json
            dailyData = {
                "Adj Close": data["Adj Close"].iloc[-1],
                "Open": data["Open"].iloc[0],
                "High": data["High"].max(),
                "Low" : data["Low"].min(),
                "Close" : data["Close"].iloc[-1]
                }
        
        ##"""print(data)
            with open('static/data.json') as fileData:
                file = fileData.read()
                if file.strip:
                    newData = json.loads(file)
                    print("Arquivo carregado")
                else:
                    print("Arquivo vazio")
                    newData = {}
        
            if i not in newData:
                newData[i] = {self.hj.strftime('%Y-%m-%d'): dailyData}
            else:
                if self.hj.strftime('%Y-%m-%d') not in newData[i]:
                    newData[i][self.hj.strftime('%Y-%m-%d')] = dailyData
                else:
                    for key, value in dailyData.items():
                        newData[i][self.hj.strftime('%Y-%m-%d')][key] = value
        
            with open('static/data.json','w') as file:
                json.dump(newData,file)

        print("Atualizando dados...")
        alert = Notification(app_id="Gecko", title="Novas atualizações", duration="short", launch="")
        alert.show()
        pass


