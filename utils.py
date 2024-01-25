import pandas as pd
import streamlit as st
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
from datetime import timedelta
import plotly.graph_objects as go
import base64

@st.cache_data
def webscraping(url,coluna):
    dados = pd.read_html(url, encoding='utf-8', decimal=',')
    dados = dados[2]
    dados.columns = dados.iloc[0]
    dados = dados[1:]
    dados = dados.rename(columns={dados.columns[1]: coluna})
    dados['Data'] = pd.to_datetime(dados['Data'], format = '%d/%m/%Y')
    dados[dados.columns[1]] = dados[dados.columns[1]].astype(float)
    dados[dados.columns[1]]= dados[dados.columns[1]]/100
    dados.set_index('Data', inplace = True)
    dados.sort_index(ascending=True, inplace=True)
    if coluna == 'Preco':
        dados.to_csv('dados_preco_petroleo.csv', encoding="utf-8")
    else:
        dados.to_csv('dados_taxa_cambio.csv', encoding="utf-8")
    return dados

def leitura_csv(arquivo):
    dados = pd.read_csv(arquivo, encoding='utf-8')
    dados['Data'] = pd.to_datetime(dados['Data'], format = '%Y-%m-%d')
    dados[dados.columns[1]] = dados[dados.columns[1]].astype(float)
    dados.set_index('Data', inplace = True)
    dados.sort_index(ascending=True, inplace=True)
    return dados

def decomposicao(dados,resultado):
    st.subheader('Série Temporal Original')
    st.line_chart(dados)
    st.subheader('Tendência')
    st.line_chart(resultado.trend)
    st.subheader('Sazonalidade')
    st.line_chart(resultado.seasonal)
    st.subheader('Residual')
    st.line_chart(resultado.resid)

@st.cache_resource
def modelo_ets(dados, qt_dias):
  dados = dados.tail(qt_dias)
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

  # Loop através dos parâmetros
  for trend in parametros_grid['trend']:
      for seasonal in parametros_grid['seasonal']:
          for seasonal_periods in parametros_grid['seasonal_periods']:
              # Criando o modelo ETS
              modelo_ets = ExponentialSmoothing(dados['Preco'], trend=trend, seasonal=seasonal, seasonal_periods=seasonal_periods)

              # Iterando sobre diferentes janelas de treinamento
              for train_index, test_index in tscv.split(dados):
                  dados_treino, dados_teste = dados.iloc[train_index], dados.iloc[test_index]

                  # Treinando o modelo
                  resultado = modelo_ets.fit()

                  # Fazendo previsões
                  previsao = resultado.forecast(steps=len(dados_teste))

                  # Calculando o MAE
                  mae = mean_absolute_error(dados_teste['Preco'].values, previsao)

              # Atualizando os melhores parâmetros se este conjunto tiver um MAE menor
              if mae < melhor_mae:
                  melhor_mae = mae
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

def colunas_ets(melhores_dados_teste,melhores_dados_treinamento,melhor_mae,melhores_parametros):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Data inicial da análise', melhores_dados_treinamento.index.min().strftime('%d-%m-%Y'))
        st.metric('MAE', melhor_mae.round(2))
    with col2:
        st.metric('Data final da análise', melhores_dados_teste.index.max().strftime('%d-%m-%Y'))
        st.metric('Tendência', melhores_parametros['trend'])
    with col3:
        st.metric('Qtd dias treinados', len(melhores_dados_treinamento))
        st.metric('Sazonalidade', melhores_parametros['seasonal'])
    with col4:
        st.metric('Qtd dias testados', len(melhores_dados_teste))
        st.metric('Períodos Sazonais', melhores_parametros['seasonal_periods'])
    
    st.markdown('<h3> Dados da previsão - Próximos 60 dias</h3>', unsafe_allow_html = True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Data prevista de maior pico', 'xpto')
    with col2:
        st.metric('Valor do maior pico','xpto')
    with col3:
        st.metric('Data prevista de menor pico', 'xpto')
    with col4:
        st.metric('Valor do menor pico','xpto')
    

def gerar_conteudo_download(dados):
    csv = dados.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f"data:file/csv;base64,{b64}"

def graf_dois_eixos(x,y1,y2):
    # Criar um objeto de figura
    fig = go.Figure()
    # Adicionar a primeira linha com eixo y à esquerda
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='Preço do barril de Petróleo (US$)', yaxis='y1'))
    # Adicionar a segunda linha com eixo y à direita
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='Taxa de Câmbio (R$/US$)', yaxis='y2'))
    # Atualizar o layout para mostrar os dois eixos y
    fig.update_layout(
        yaxis=dict(title='Preço do barril de Petróleo (US$)', side='left'),
        yaxis2=dict(title='Taxa de Câmbio (R$/US$)', overlaying='y', side='right'),
        legend=dict(orientation='h', y=1.1, x=0.5, xanchor='center', yanchor='top')
    )
    return fig

