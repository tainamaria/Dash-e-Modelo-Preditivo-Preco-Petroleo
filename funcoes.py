import pandas as pd

def leitura_csv(arquivo):
    dados = pd.read_csv(arquivo, encoding='utf-8')
    dados['Data'] = pd.to_datetime(dados['Data'], format = '%Y-%m-%d')
    dados[dados.columns[1]] = dados[dados.columns[1]].astype(float)
    dados.set_index('Data', inplace = True)
    dados.sort_index(ascending=True, inplace=True)
    return dados