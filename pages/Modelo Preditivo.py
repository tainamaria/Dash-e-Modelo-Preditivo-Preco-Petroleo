## IMPORTAÇÃO ARQUIVOS
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error,mean_squared_error
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title= 'Modelo Preditivo - Preço dos Combustíveis', layout='wide', page_icon= ':fuelpump:')
st.title('Modelo Preditivo :telescope:')

# Carregamento do conjunto de dados atualizado, para isso basta declarar uma variável e passar o caminho que o arquivo que se encontra.
dados = pd.read_html('http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view', encoding='utf-8', decimal=',')
dados = dados[2]
dados.columns = dados.iloc[0]
dados = dados[1:]
dados = dados.rename(columns={'Preço - petróleo bruto - Brent (FOB)': 'Preco'})
dados['Data'] = pd.to_datetime(dados['Data'], format = '%d/%m/%Y')
dados.Preco = dados.Preco.astype(float)
dados.Preco = dados.Preco/100
dados.set_index('Data', inplace = True)
dados.sort_index(ascending=True, inplace=True)

def ets_com_periodo(dados, data_inicial, data_final):
    data_ets = dados[(dados.index >= data_inicial) & ( dados.index <= data_final)]
    train_size = int(0.80 * len(data_ets))
    train_df = data_ets[:train_size]
    test_df = data_ets[train_size:]
    # Gerando o modelo da base de treino para sazonalidade multiplicativa e aditiva
    fit_mult_train = ExponentialSmoothing(train_df, seasonal_periods=int(len(train_df)/2), trend='multiplicative', seasonal='additive').fit() # usando seasonal 'multiplicative'
    fit_adit_train = ExponentialSmoothing(train_df, seasonal_periods=int(len(train_df)/2), trend='additive', seasonal='additive').fit() #usando seasonal 'adittive' pq a sazonalidade é constante
    mae_multiplicativo = mean_absolute_error(test_df['Preco'], fit_mult_train.forecast(len(test_df)))
    mse_multiplicativo = mean_squared_error(test_df['Preco'], fit_mult_train.forecast(len(test_df)))
    mae_aditivo = mean_absolute_error(test_df['Preco'], fit_adit_train.forecast(len(test_df)))
    mse_aditivo = mean_squared_error(test_df['Preco'], fit_adit_train.forecast(len(test_df)))
    return mae_multiplicativo,mse_multiplicativo,mae_aditivo,mse_aditivo,train_df,test_df

def ets_sem_periodo(dados):
  dados = dados.tail(365)
  # Definindo os parâmetros a serem testados
  parametros_grid = {
      'trend': ['add', 'additive', 'mul', 'multiplicative'],
      'seasonal': ['add', 'additive', 'mul', 'multiplicative'],
      'seasonal_periods': [30],  # Assumindo um padrão sazonal mensal
  }

  # Configurando a validação cruzada de séries temporais
  tscv = TimeSeriesSplit(n_splits=5)

  # Inicializando as variáveis para armazenar os melhores resultados
  melhor_mae = float('inf')
  melhores_parametros = None
  melhor_df_treino = None
  melhor_df_teste = None

  # Loop através dos parâmetros
  for trend in parametros_grid['trend']:
      for seasonal in parametros_grid['seasonal']:
          for seasonal_periods in parametros_grid['seasonal_periods']:
              # Criando o modelo ETS
              modelo_ets = ExponentialSmoothing(dados['Preco'], trend=trend, seasonal=seasonal, seasonal_periods=seasonal_periods)

              # Inicializando as variáveis para armazenar o MAE
              mae_total = 0

              # Iterando sobre diferentes janelas de treinamento
              for train_index, test_index in tscv.split(dados):
                  dados_treino, dados_teste = dados.iloc[train_index], dados.iloc[test_index]

                  # Treinando o modelo
                  resultado = modelo_ets.fit()

                  # Fazendo previsões
                  previsao = resultado.forecast(steps=len(dados_teste))

                  # Calculando o MAE
                  mae = mean_absolute_error(dados_teste['Preco'].values, previsao)
                  mae_total += mae

              # Calculando a média do MAE para este conjunto de parâmetros
              mae_medio = mae_total / tscv.n_splits

              # Atualizando os melhores parâmetros se este conjunto tiver um MAE menor
              if mae_medio < melhor_mae:
                  melhor_mae = mae_medio
                  melhores_parametros = {'trend': trend, 'seasonal': seasonal, 'seasonal_periods': seasonal_periods}
                  melhores_dados_treinamento = dados_treino
                  melhores_dados_teste = dados_teste
                  melhor_resultado_fit = resultado

  # Imprimindo os melhores parâmetros e o MAE correspondente
  print(f'Melhores Parâmetros: {melhores_parametros}')
  print(f'MAE para os melhores parâmetros: {melhor_mae}')
  print(f'MAE para os melhor treino: {len(melhores_dados_treinamento)}')
  print(f'MAE para os melhor teste: {len(melhores_dados_teste)}')
  return melhor_mae, melhores_parametros, melhores_dados_teste, melhores_dados_treinamento, melhor_resultado_fit

# Gráfico de comparação entre os dados históricos, testados e previstos
def graf_comparativo(dados_historicos_x,dados_historicos_y,dados_testados_x,dados_testados_y,dados_previstos_x,dados_previstos_y,titulo):
  fig = go.Figure()
  # Dados históricos
  fig.add_trace(go.Scatter(x = dados_historicos_x, y = dados_historicos_y, name = 'Dados históricos'))
  # Dados testados
  fig.add_trace(go.Scatter(x = dados_testados_x, y = dados_testados_y, name = 'Dados testados'))
  # Dados previstos
  fig.add_trace(go.Scatter(x = dados_previstos_x, y = dados_previstos_y, name = 'Dados previstos'))

  fig.update_layout(title= titulo,
  xaxis_title='Data',
  yaxis_title='Fechamento',
  font = {'family': 'Arial','size': 16,'color': 'black'})
  fig.update_xaxes( showgrid=True, gridwidth=1, gridcolor='lightgray',
  showline=True, linewidth=1, linecolor='black')
  fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray',
  showline=True, linewidth=1, linecolor='black')
  return fig

# Futuros dias úteis da semana
def dias_uteis_futuros(data_inicial,qtd_dias):
  dias_uteis = []

  while len(dias_uteis) < qtd_dias:
      data_inicial += timedelta(days=1)  # Avança um dia de cada vez
      # Verifica se o dia da semana não é sábado (5) nem domingo (6)
      if data_inicial.weekday() not in [5, 6]:
          dias_uteis.append(data_inicial)
  return dias_uteis

algoritmo = st.sidebar.selectbox("Selecione o algoritmo", ['ETS','Prophet','Regressão Linear'])
periodo = st.sidebar.checkbox('Escolher o período dos dados de treino e teste')
if algoritmo == 'ETS':
    if periodo:
        st.header('ETS - Error Tren Seasonality')
        data_inicial = st.sidebar.date_input('Data inicial', date.today())
        data_final = st.sidebar.date_input('Data final', date.today())
        # mae_multiplicativo,mse_multiplicativo,mae_aditivo,mse_aditivo,train_df,test_df = ets_com_periodo(dados, data_inicial, data_final)
    else:
        st.header('ETS - Error Tren Seasonality')
        melhor_mae, melhores_parametros, melhores_dados_teste, melhores_dados_treinamento, fit_train = ets_sem_periodo(dados)
        col1, col2, col3 = st.columns(3)
        with col1: #utilizando a cláusula with, mas poderíamos escrever apenas "col1." antes da métrica
            st.metric('Menor MAE', melhor_mae.round(2)) #identado para ficar dentro do with
            st.metric('Tendência', melhores_parametros['trend'])
        with col2:
            st.metric('Qtd dias treinados', len(melhores_dados_treinamento))
            st.metric('Sazonalidade', melhores_parametros['seasonal'])
        with col3:
            st.metric('Qtd dias testados', len(melhores_dados_teste))
            st.metric('Períodos Sazonais', melhores_parametros['seasonal_periods'])

        dias_futuros = dias_uteis_futuros(dados.index.max(),90)
        
        figura = graf_comparativo(dados.index.to_numpy(),dados['Preco'].to_numpy(),melhores_dados_teste.index.to_numpy(),fit_train.forecast(len(melhores_dados_teste)).to_numpy(),dias_futuros,fit_train.forecast(90).to_numpy(),'Dados históricos x Previsões')

        st.plotly_chart(figura) 