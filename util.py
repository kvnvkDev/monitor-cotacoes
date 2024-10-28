
import hashlib
import os


# Função para criar o hash baseado no ticker e no período
def create_cache_key(ticker, period, data):
    return hashlib.md5(f'{ticker}_{period}_{data}'.encode()).hexdigest()

# Função para salvar o gráfico em cache
def save_plot_cache(ticker, period, fig, data):
    cache_key = create_cache_key(ticker, period, data)
    cache_dir = 'cache'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    fig.savefig(os.path.join(cache_dir, f'{cache_key}.png'))

# Função para carregar o gráfico do cache
def load_plot_cache(ticker, period, data):
    cache_key = create_cache_key(ticker, period, data)
    cache_path = os.path.join('cache', f'{cache_key}.png')
    if os.path.exists(cache_path):
        return cache_path
    return None

def limpar_pasta_cache():
    caminho = 'cache'
    for arquivo in os.listdir(caminho):
        caminho_arquivo = os.path.join(caminho, arquivo)
        if os.path.isfile(caminho_arquivo):
            os.remove(caminho_arquivo)