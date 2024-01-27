import pandas as pd
import streamlit as st
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
from datetime import timedelta
import plotly.graph_objects as go
import time
import numpy as np
# from pmdarima.arima import auto_arima
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

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

def atualiza_dados():
    if st.sidebar.button("###### Clique para atualizar os dados da aplicação"):
        # Limpa o cache de dados
        st.cache_data.clear()
        st.cache_resource.clear()

def decomposicao(dados,resultado):
    st.subheader('Série Temporal Original')
    st.line_chart(dados)
    st.subheader('Tendência')
    st.markdown('<p style="text-align: justify;">Quando falamos sobre tendência na decomposição de uma série temporal, estamos interessados em identificar padrões de crescimento ou declínio que ocorrem ao longo de um período de tempo significativo, ignorando as variações sazonais e flutuações aleatórias que podem ocorrer em escalas de tempo menores.</p>', unsafe_allow_html = True)
    st.line_chart(resultado.trend)
    st.subheader('Sazonalidade')
    st.markdown('<p style="text-align: justify;">A sazonalidade indica variações sistemáticas que ocorrem em determinados momentos ou períodos do ano e são independentes da tendência de longo prazo e das flutuações aleatórias na série temporal. Ela reflete regularidades que podem ser observadas ao longo de múltiplos ciclos sazonais.</p>', unsafe_allow_html = True)
    st.line_chart(resultado.seasonal)
    st.subheader('Residual')
    st.markdown('<p style="text-align: justify;">Na decomposição de uma série temporal, o resíduo (também conhecido como erro ou componente aleatório) é a parte da série que não pode ser explicada pela tendência de longo prazo e pela sazonalidade. Em outras palavras, o resíduo representa as flutuações irregulares e imprevisíveis que não seguem nenhum padrão discernível na série temporal.</p>', unsafe_allow_html = True)
    st.line_chart(resultado.resid)

def teste_estatistico(dados,string_teste):
    st.subheader('Testes Estatísticos')
    st.markdown('<p style="text-align: justify;">O teste de Dickey-Fuller Aumentado (ADF), frequentemente implementado na função adfuller do pacote statsmodels em Python, é um teste estatístico utilizado para determinar se uma série temporal é estacionária ou não. Uma série temporal é considerada estacionária quando suas propriedades estatísticas, como média e variância, permanecem constantes ao longo do tempo. Em outras palavras, não há padrões sistemáticos ou tendências discerníveis na série que afetem sua média ou variância.</p>', unsafe_allow_html = True)

    st.markdown(f'<p style="text-align: justify;"><span style="font-weight: bold">{string_teste}</span></p>', unsafe_allow_html = True)
    # Realizar o teste de Dickey-Fuller Aumentado
    resultado_adf = adfuller(dados)
    st.markdown(f'<p style="text-align: justify;">Estatística do teste ADF: {resultado_adf[0]}.</p>', unsafe_allow_html = True)
    st.markdown(f'<p style="text-align: justify;">Valor-p: {resultado_adf[1]}.</p>', unsafe_allow_html = True)
    st.markdown(f'<p style="text-align: justify;">Valores críticos:</p>', unsafe_allow_html = True)
    for chave, valor in resultado_adf[4].items():
        st.markdown(f'<p style="text-align: justify;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{chave}: {valor}.</p>', unsafe_allow_html = True)
    st.markdown('<p style="text-align: justify;">Se o valor-p for menor que o nível de significância escolhido (geralmente 0.05), rejeitamos a hipótese nula e concluímos que a série é estacionária. Caso contrário, não rejeitamos a hipótese nula e inferimos que a série não é estacionária. Isso significa que a série possui tendência.</p>', unsafe_allow_html = True)
    # Interpretar o resultado do teste
    if resultado_adf[1] < 0.05:
        st.markdown(f'<p style="text-align: justify;">Dessa forma, a série temporal é estacionária (rejeitamos a hipótese nula).</p>', unsafe_allow_html = True)
    else:
        st.markdown(f'<p style="text-align: justify;">Dessa forma, a série temporal não é estacionária (falhamos em rejeitar a hipótese nula).</p>', unsafe_allow_html = True)

    st.subheader('Gráficos de autocorrelação')
    st.markdown(f'<p style="text-align: justify;">Para identificar a presença de sazonalidade nos gráficos de autocorrelação simples (ACF) e autocorrelação parcial (PACF), é possível procurar padrões de picos significativos em intervalos regulares.</p>', unsafe_allow_html = True)
    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Autocorrelação Simples (ACF):</span> os picos indicam a correlação entre a série temporal atual e suas observações passadas em vários lags. Se houver picos significativos em intervalos regulares, isso sugere a presença de sazonalidade na série temporal.</p>', unsafe_allow_html = True)
    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Autocorrelação Parcial (PACF):</span> os picos representam a correlação entre a série temporal atual e suas observações passadas, removendo o efeito das observações intermediárias. Picos significativos em intervalos regulares no PACF também indicam a presença de sazonalidade.</p>', unsafe_allow_html = True)

    # col1, col2 = st.columns(2)
    # with col1:
    #     fig, ax = plt.subplots()
    #     plot_acf(dados, ax=ax)
    #     plt.xlabel('Lag')
    #     plt.ylabel('ACF')
    #     plt.title('Função de Autocorrelação (ACF)')
    #     fig.patch.set_alpha(0)
    #     st.pyplot(fig)
    # with col2:
    #     fig, ax = plt.subplots()
    #     plot_pacf(dados, ax=ax)
    #     plt.xlabel('Lag')
    #     plt.ylabel('PACF')
    #     plt.title('Função de Autocorrelação (PACF)')
    #     fig.patch.set_alpha(0)
    #     st.pyplot(fig)

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

  return melhor_mae, melhores_parametros, melhores_dados_teste, melhores_dados_treinamento, melhor_resultado_fit

# @st.cache_resource
# def modelo_arima(dados,qt_dias_previsao):
#     dados = dados.tail(365) # Últimos 365 anos
#     # Dividir os dados em treino e teste
#     dados_treino = dados.iloc[:-qt_dias_previsao]  # Treinamento: todos os dados exceto os últimos qt_dias_previsao dias
#     dados_teste = dados.iloc[-qt_dias_previsao:]   # Teste: últimos qt_dias_previsao dias

#     # Ajustar o modelo ARIMA usando auto_arima
#     modelo_arima_teste = auto_arima(dados_treino['Preco'], seasonal=False, trace=True) 

#     # Fazer a previsão dos próximos qt_dias_previsao dias
#     previsao = modelo_arima_teste.predict(n_periods=qt_dias_previsao)

#     # Calcular o erro MAE para a previsão
#     melhor_mae = mean_absolute_error(dados_teste['Preco'], previsao)

#     # Ajustar modelo para os últimos dias
#     modelo_arima= auto_arima(dados['Preco'], seasonal=False, trace=True) 

#     return melhor_mae, dados_teste, dados_treino, modelo_arima_teste, modelo_arima

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
  yaxis_title='Preço (US$)',
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

cor_estilizada = 'color: #0145AC;'
fonte_negrito = 'font-weight: bold;'

def colunas_ets(melhores_dados_teste,melhores_dados_treinamento,melhor_mae,melhores_parametros,df_forecasting,qt_dias_previsao):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric1 = melhores_dados_treinamento.index.min().strftime('%d/%m/%Y')
        st.markdown(f"<h2 style='{cor_estilizada}'>{metric1}</h2> <span style='{fonte_negrito}'> Data inicial da análise </span>", unsafe_allow_html=True)
        metric2 = melhor_mae.round(2)
        st.markdown(f"<h2 style='{cor_estilizada}'>{metric2}</h2> <span style='{fonte_negrito}'> MAE </span>", unsafe_allow_html=True)
    with col2:
        metric3 = melhores_dados_teste.index.max().strftime('%d/%m/%Y')
        st.markdown(f"<h2 style='{cor_estilizada}'>{metric3}</h2> <span style='{fonte_negrito}'> Data final da análise </span>", unsafe_allow_html=True)
        metric4 = melhores_parametros['trend']
        st.markdown(f"<h2 style='{cor_estilizada}'>{metric4}</h2> <span style='{fonte_negrito}'> Tendência </span>", unsafe_allow_html=True)
    with col3:
        metric5 = len(melhores_dados_treinamento)
        st.markdown(f"<h2 style='{cor_estilizada}'>{metric5}</h2> <span style='{fonte_negrito}'> Qtd dias treinados </span>", unsafe_allow_html=True)
        metric6 = melhores_parametros['seasonal']
        st.markdown(f"<h2 style='{cor_estilizada}'>{metric6}</h2> <span style='{fonte_negrito}'> Sazonalidade </span>", unsafe_allow_html=True)
    with col4:
        metric7 = len(melhores_dados_teste)
        st.markdown(f"<h2 style='{cor_estilizada}'>{metric7}</h2> <span style='{fonte_negrito}'> Qtd dias testados </span>", unsafe_allow_html=True)
        metric8 = melhores_parametros['seasonal_periods']
        st.markdown(f"<h2 style='{cor_estilizada}'>{metric8}</h2> <span style='{fonte_negrito}'> Períodos Sazonais </span>", unsafe_allow_html=True)

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)   
    st.markdown(f'<h3> Dados da previsão - Próximos {qt_dias_previsao} dias</h3>', unsafe_allow_html = True)

    df_forecasting['Data'] = pd.to_datetime(df_forecasting['Data'], format = '%d/%m/%Y')
    df_forecasting.set_index('Data', inplace = True)

    preco_min = df_forecasting['Preco'].min()
    data_preco_min = df_forecasting[df_forecasting['Preco']==preco_min].index

    preco_max = df_forecasting['Preco'].max()
    data_preco_max = df_forecasting[df_forecasting['Preco']==preco_max].index

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric9 = data_preco_max[0].strftime('%d/%m/%Y')
        st.markdown(f"<h2 style='{cor_estilizada}'>{metric9}</h2> <span style='{fonte_negrito}'> Data prevista de maior pico </span>", unsafe_allow_html=True)
    with col2:
        metric10 = preco_max.round(2)
        st.markdown(f"<h2 style='{cor_estilizada}'>{metric10}</h2> <span style='{fonte_negrito}'> Valor do maior pico </span>", unsafe_allow_html=True)
    with col3:
        metric11 = data_preco_min[0].strftime('%d/%m/%Y')
        st.markdown(f"<h2 style='{cor_estilizada}'>{metric11}</h2> <span style='{fonte_negrito}'> Data prevista de menor pico </span>", unsafe_allow_html=True)
    with col4:
        metric12 = preco_min.round(2)
        st.markdown(f"<h2 style='{cor_estilizada}'>{metric12}</h2> <span style='{fonte_negrito}'> Valor do menor pico </span>", unsafe_allow_html=True)

# def colunas_arima(melhor_mae, dados_teste, dados_treino, modelo_arima_teste, df_forecasting, qt_dias_previsao):
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         metric13 = dados_treino.index.min().strftime('%d/%m/%Y')
#         st.markdown(f"<h2 style='{cor_estilizada}'>{metric13}</h2> <span style='{fonte_negrito}'> Data inicial da análise </span>", unsafe_allow_html=True)
#         metric14 = melhor_mae.round(2)
#         st.markdown(f"<h2 style='{cor_estilizada}'>{metric14}</h2> <span style='{fonte_negrito}'> MAE </span>", unsafe_allow_html=True)
#     with col2:
#         metric15 = dados_teste.index.max().strftime('%d/%m/%Y')
#         st.markdown(f"<h2 style='{cor_estilizada}'>{metric15}</h2> <span style='{fonte_negrito}'> Data final da análise </span>", unsafe_allow_html=True)
#         metric16 = modelo_arima_teste.order[0]
#         st.markdown(f"<h2 style='{cor_estilizada}'>{metric16}</h2> <span style='{fonte_negrito}'> p </span>", unsafe_allow_html=True)
#     with col3:
#         metric17 = len(dados_treino)
#         st.markdown(f"<h2 style='{cor_estilizada}'>{metric17}</h2> <span style='{fonte_negrito}'> Qtd dias treinados </span>", unsafe_allow_html=True)
#         metric18 = modelo_arima_teste.order[1]
#         st.markdown(f"<h2 style='{cor_estilizada}'>{metric18}</h2> <span style='{fonte_negrito}'> d </span>", unsafe_allow_html=True)
#     with col4:
#         metric19 = len(dados_teste)
#         st.markdown(f"<h2 style='{cor_estilizada}'>{metric19}</h2> <span style='{fonte_negrito}'> Qtd dias testados </span>", unsafe_allow_html=True)
#         metric20 = modelo_arima_teste.order[2]
#         st.markdown(f"<h2 style='{cor_estilizada}'>{metric20}</h2> <span style='{fonte_negrito}'> q </span>", unsafe_allow_html=True)

#     st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)  
#     st.markdown(f'<h3> Dados da previsão - Próximos {qt_dias_previsao} dias</h3>', unsafe_allow_html = True)

#     df_forecasting['Data'] = pd.to_datetime(df_forecasting['Data'], format = '%d/%m/%Y')
#     df_forecasting.set_index('Data', inplace = True)

#     preco_min = df_forecasting['Preco'].min()
#     data_preco_min = df_forecasting[df_forecasting['Preco']==preco_min].index

#     preco_max = df_forecasting['Preco'].max()
#     data_preco_max = df_forecasting[df_forecasting['Preco']==preco_max].index

#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         metric21 = data_preco_max[0].strftime('%d/%m/%Y')
#         st.markdown(f"<h2 style='{cor_estilizada}'>{metric21}</h2> <span style='{fonte_negrito}'> Data prevista de maior pico </span>", unsafe_allow_html=True)

#         #st.metric('Data prevista de maior pico', data_preco_max[0].strftime('%d/%m/%Y'))
#     with col2:
#         metric22 = preco_max.round(2)
#         st.markdown(f"<h2 style='{cor_estilizada}'>{metric22}</h2> <span style='{fonte_negrito}'> Valor do maior pico </span>", unsafe_allow_html=True)

#         #st.metric('Valor do maior pico', preco_max.round(2))
#     with col3:
#         metric23 = data_preco_min[0].strftime('%d/%m/%Y')
#         st.markdown(f"<h2 style='{cor_estilizada}'>{metric23}</h2> <span style='{fonte_negrito}'> Data prevista de menor pico </span>", unsafe_allow_html=True)


#         #st.metric('Data prevista de menor pico', data_preco_min[0].strftime('%d/%m/%Y'))
#     with col4:
#         metric24 = preco_min.round(2)
#         st.markdown(f"<h2 style='{cor_estilizada}'>{metric24}</h2> <span style='{fonte_negrito}'> Valor do menor pico </span>", unsafe_allow_html=True)

#         #st.metric('Valor do menor pico', preco_min.round(2))

def gerar_conteudo_download(dados):
    return dados.to_csv(index = False).encode('utf-8')

def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso', icon="✅")
    time.sleep(10) #timer
    sucesso.empty() #apaga a mensagem após o timer

def graf_marcado_max_min(dados):
    # Encontrar índice do maior e menor Preco
    indice_maior_preco = dados['Preco'].idxmax()
    indice_menor_preco = dados['Preco'].idxmin()

    # Plotar o gráfico
    fig = go.Figure()

    # Adicionar dados de linha
    fig.add_trace(go.Scatter(x=dados['Data'], y=dados['Preco'], mode='lines',showlegend=False))

    # Adicionar pico máximo
    fig.add_trace(go.Scatter(x=[dados['Data'].loc[indice_maior_preco]], y=[dados['Preco'].loc[indice_maior_preco]],
                            mode='markers', name='Máximo', marker=dict(color='red', size=10)))

    # Adicionar pico mínimo
    fig.add_trace(go.Scatter(x=[dados['Data'].loc[indice_menor_preco]], y=[dados['Preco'].loc[indice_menor_preco]],
                            mode='markers', name='Mínimo', marker=dict(color='green', size=10)))

    # Atualizar layout do gráfico
    fig.update_layout(title='Preço por barril de Petróleo ao longo do tempo',
                    xaxis_title='Data', yaxis_title='Preço (US$)',legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center', yanchor='top'))
    
    return fig

def graf_marcado_multiplos(x, y, picos_indices_max, picos_indices_min,y2):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Preço do barril de Petróleo (US$)'))

    # Adiciona a série de picos mais altos apenas uma vez
    if np.any(picos_indices_max):
        x_max = [x[i] for i in picos_indices_max]
        y_max = [y[i] for i in picos_indices_max]
        fig.add_trace(go.Scatter(x=x_max, y=y_max, mode='markers', name='Máximos', marker=dict(color='red', size=10)))

    # Adiciona a série de picos mais baixos apenas uma vez
    if np.any(picos_indices_min):
        x_min = [x[i] for i in picos_indices_min]
        y_min = [y[i] for i in picos_indices_min]
        fig.add_trace(go.Scatter(x=x_min, y=y_min, mode='markers', name='Mínimos', marker=dict(color='green', size=10)))

    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='Taxa de Câmbio (R$/US$)', yaxis='y2'))

    fig.update_layout( title='Preço do barril de Petróleo x Taxa de Câmbio',
        yaxis=dict(title='Preço do barril de Petróleo (US$)', side='left'),
        yaxis2=dict(title='Taxa de Câmbio (R$/US$)', overlaying='y', side='right'),
        legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center', yanchor='top')
    )
    return fig