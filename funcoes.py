import pandas as pd
# import streamlit as st
# from statsmodels.tsa.holtwinters import ExponentialSmoothing
# from sklearn.metrics import mean_absolute_error
# from sklearn.model_selection import TimeSeriesSplit
# from datetime import timedelta
# import plotly.graph_objects as go
# import time
# import numpy as np
# # from pmdarima.arima import auto_arima
# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# import matplotlib.pyplot as plt
# from statsmodels.tsa.stattools import adfuller

# def webscraping(url,coluna):
#     dados = pd.read_html(url, encoding='utf-8', decimal=',')
#     dados = dados[2]
#     dados.columns = dados.iloc[0]
#     dados = dados[1:]
#     dados = dados.rename(columns={dados.columns[1]: coluna})
#     dados['Data'] = pd.to_datetime(dados['Data'], format = '%d/%m/%Y')
#     dados[dados.columns[1]] = dados[dados.columns[1]].astype(float)
#     dados[dados.columns[1]]= dados[dados.columns[1]]/100
#     dados.set_index('Data', inplace = True)
#     dados.sort_index(ascending=True, inplace=True)
#     if coluna == 'Preco':
#         dados.to_csv('dados_preco_petroleo.csv', encoding="utf-8")
#     else:
#         dados.to_csv('dados_taxa_cambio.csv', encoding="utf-8")
#     return dados

def leitura_csv(arquivo):
    dados = pd.read_csv(arquivo, encoding='utf-8')
    dados['Data'] = pd.to_datetime(dados['Data'], format = '%Y-%m-%d')
    dados[dados.columns[1]] = dados[dados.columns[1]].astype(float)
    dados.set_index('Data', inplace = True)
    dados.sort_index(ascending=True, inplace=True)
    return dados