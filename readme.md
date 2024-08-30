# Monitor de cotações

Esta é uma aplicação web em Python para monitorar o preço de ativos na bolsa de valores. Possui um script que roda em segundo plano capturando os dados da biblioteca yfinance e armazena alguns dados para histórico de preços. E também possui uma interface web com back-end Flask que permite ver os dados a medida que são baixados com gráficos gerados pela biblioteca matplotlib.

A aplicação permite configurar o período de tempo que os dados serão baixados e exibe uma notificação no sistema para informar o usuário. É possivel adicionar ou remover tickers conforme a prefêrencia do usuário. As páginas web possui design responsivo, se adaptando a diferentes tamanhos de telas.

## Tecnologias utilizadas
- Python 3.11
- HTML
- JavaScript
- CSS

### Dependências
- flask 3.0.3
- yfinance
- matplotlib
- winotify


## Instalar e executar

Para começar é preciso ter o python e as dependências do projeto instalados.

[Download Python](https://www.python.org/downloads/)

Instalar dependências: 

` pip install flask yfinance matplotlib winotify `

Use o comando abaixo para clonar o repositório

` git clone https://github.com/kvnvkDev/monitor-cotacoes `

Após a instalação do python e das dependências, pelo terminal navegue até a pasta do repositório e execute o arquivo initApp.py

` python initApp.py `

O arquivo initApp.py vai iniciar o script de captura dos dados e o servidor web do flask. Para acessar a aplicação basta acessar o link http://127.0.0.1:5000 em qualquer navegador.

Este aplicativo usa dados extraidos do yfinance. O nome dos tickers adicionados devem seguir a nomenclatura do Yahoo Finance.
Os tickers usados neste repositório são apenas como exemplo e não são uma recomendação de investimento.
