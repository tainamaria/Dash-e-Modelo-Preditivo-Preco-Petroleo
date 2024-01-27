## IMPORTAÇÃO ARQUIVOS
import streamlit as st
import pandas as pd
import numpy as np
from utils import leitura_csv,modelo_ets,graf_comparativo,dias_uteis_futuros,gerar_conteudo_download,mensagem_sucesso,graf_duas_linhas,modelo_ets_previsao

st.set_page_config(page_title= 'Modelo - Predição', layout='wide', page_icon= ':fuelpump:')
st.title('Modelo Preditivo :telescope:')

st.markdown('<p style="text-align: justify;">Considerando que os dados apresentaram uma leve repetição sazonal a cada intervalo de 30 dias, optamos por utilizar o modelo <span style="font-weight: bold">ETS (Erro, Tendência, Sazonalidade)</span>. O modelo ETS é adequado para séries temporais com características variáveis no tempo, permitindo a captura de padrões complexos mesmo em situações onde as tendências e sazonalidades são mínimas. Além disso, o modelo ETS oferece uma estrutura flexível que pode ser adaptada para se ajustar às particularidades dos dados, garantindo uma modelagem precisa e robusta.</p>', unsafe_allow_html = True)

st.header('Parâmetros')
st.markdown('<p style="text-align: justify;">ETS é um modelo de séries temporais que descreve a evolução de uma variável ao longo do tempo, levando em consideração três parâmetros principais: tendência, sazonalidade e períodos sazonais.  </p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Tendência (trend):</span> O parâmetro "trend" determina como a tendência é modelada no modelo ETS. Existem duas opções para a tendência:</p>', unsafe_allow_html = True)
st.markdown('* "add" ou "additive": Indica que a tendência é aditiva, ou seja, a variação da tendência é constante ao longo do tempo.', unsafe_allow_html = True)
st.markdown('* "mul" ou "multiplicative": Indica que a tendência é multiplicativa, o que significa que a variação da tendência é proporcional ao nível da série temporal.', unsafe_allow_html = True)

st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Sazonalidade (seasonal):</span> O parâmetro "seasonal" determina como a sazonalidade é modelada no modelo ETS. Assim como com a tendência, existem duas opções para a sazonalidade:</p>', unsafe_allow_html = True)
st.markdown('* "add" ou "additive": Indica que a sazonalidade é aditiva, ou seja, a variação sazonal é constante ao longo do tempo.', unsafe_allow_html = True)
st.markdown('* "mul" ou "multiplicative": Indica que a sazonalidade é multiplicativa, o que significa que a variação sazonal é proporcional ao nível da série temporal.', unsafe_allow_html = True)

st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Períodos Sazonais (seasonal_periods):</span> O parâmetro "seasonal_periods" indica o número de períodos em uma temporada ou ciclo sazonal.</p>', unsafe_allow_html = True) 
st.markdown('Por exemplo, se os dados forem diários e houver uma sazonalidade mensal, o número de períodos sazonais seria 30.', unsafe_allow_html = True)

st.header('Performance do modelo')
st.markdown('<p style="text-align: justify;">Para a divisão dos dados em treinamento e teste foi utilizado o <span style="font-weight: bold">TimeSeriesSplit</span>, uma técnica de validação cruzada especializada para séries temporais. O TimeSeriesSplit divide os dados em conjuntos de treinamento e teste mantendo a ordem temporal. Ao avaliar o modelo em múltiplas divisões temporais, você obtém uma estimativa mais robusta do desempenho médio do modelo ao longo do tempo. Isso pode ajudar a reduzir o viés de avaliação e fornecer uma avaliação mais confiável do modelo.</p>', unsafe_allow_html = True) 
st.markdown('Além disso, é possível comparar as diferentes combinações de parâmetros do modelo e avaliar seu desempenho em termos de erro ao longo do tempo em diferentes períodos, ajudando a selecionar os modelos mais robustos e generalizáveis para a série temporal.', unsafe_allow_html = True)


## LEITURA DOS DADOS DO ARQUIVO GRAVADO
arquivo = 'dados_preco_petroleo.csv'
dados = leitura_csv(arquivo)

qt_dias_previsao = 30


st.header('Melhor resultado do Treino e Teste')
melhor_mae, melhores_parametros, melhores_dados_teste, melhores_dados_treinamento, fit_train, melhor_wmape, df_completo = modelo_ets(dados,180)

cor_estilizada = 'color: #0145AC;'
fonte_negrito = 'font-weight: bold;'

col1, col2, col3, col4 = st.columns(4)
with col1:
    metric1 = melhores_dados_treinamento.index.min().strftime('%d/%m/%Y')
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric1}</h2> <span style='{fonte_negrito}'> Data inicial da análise </span>", unsafe_allow_html=True)
    metric2 = melhor_mae.round(2)
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric2}</h2> <span style='{fonte_negrito}'> Menor MAE </span>", unsafe_allow_html=True)
with col2:
    metric3 = melhores_dados_teste.index.max().strftime('%d/%m/%Y')
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric3}</h2> <span style='{fonte_negrito}'> Data final da análise </span>", unsafe_allow_html=True)
    metric4 = f'{melhor_wmape:.2%}'
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric4}</h2> <span style='{fonte_negrito}'> WMAPE </span>", unsafe_allow_html=True)
with col3:
    metric5 = len(melhores_dados_treinamento)
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric5}</h2> <span style='{fonte_negrito}'> Qtd dias treinados </span>", unsafe_allow_html=True)
    metric6 = melhores_parametros['trend']
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric6}</h2> <span style='{fonte_negrito}'> Tendência </span>", unsafe_allow_html=True)
with col4:
    metric7 = len(melhores_dados_teste)
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric7}</h2> <span style='{fonte_negrito}'> Qtd dias testados </span>", unsafe_allow_html=True)
    metric8 = melhores_parametros['seasonal']
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric8}</h2> <span style='{fonte_negrito}'> Sazonalidade </span>", unsafe_allow_html=True)

# graf_duas_linhas(melhores_dados_teste.index.to_numpy(),melhores_dados_teste['Preco'].to_numpy(),'Resutado do dados de teste e previsão')

import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(x=melhores_dados_teste.index.to_numpy(), y=melhores_dados_teste['Preco'].to_numpy(), mode='lines', name='Dados de Teste'))
fig.add_trace(go.Scatter(x=melhores_dados_teste.index.to_numpy(), y=fit_train.forecast(qt_dias_previsao).to_numpy(), mode='lines', name='Dados de Previsão do modelo'))
st.plotly_chart(fig, use_container_width=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)   
with st.expander("Visualizar todos os resultados"):
    st.write(df_completo)

st.header('Previsão') 

col1, col2, col3, col4 = st.columns(4)
with col1:
    qt_dias_historicos = st.number_input("Quantidade de dias históricos para treino", min_value=0)
with col2:
    qt_dias_prever = st.number_input("Quantidade de dias que deseja prever", min_value=0)
with col3:
    opcao_tendencia = st.selectbox("Tendência:", ['Mul', 'Add'])
with col4:
    opcao_sazonalidade = st.selectbox("Sazonalidade:", ['Mul', 'Add'])

forecasting = modelo_ets_previsao(dados, 150, 30, metric6,metric8)
df_forecasting = pd.DataFrame()
dias_futuros = dias_uteis_futuros(dados.index.max(),qt_dias_previsao)
df_forecasting['Data'] = dias_futuros
df_forecasting['Preco'] = fit_train.forecast(qt_dias_previsao).reset_index(drop=True)

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

fig = go.Figure()
fig.add_trace(go.Scatter(x=dados.tail(150).index.to_numpy(), y=dados.tail(150)['Preco'].to_numpy(), mode='lines', name='Dados Históricos'))
fig.add_trace(go.Scatter(x=dias_futuros, y=forecasting.to_numpy(), mode='lines', name='Dados de Previsão do modelo'))
st.plotly_chart(fig, use_container_width=True)

# figura = graf_comparativo(dados.tail(365).index.to_numpy(),dados.tail(365)['Preco'].to_numpy(),melhores_dados_teste.index.to_numpy(),fit_train.forecast(len(melhores_dados_teste)).to_numpy(),dias_futuros,fit_train.forecast(qt_dias_previsao).to_numpy(),'Dados históricos x Previsões')





st.markdown('Escreva um nome para o arquivo:')
col1, col2 = st.columns(2)
with col1:
    nome_arquivo = st.text_input('', label_visibility='collapsed', value='dados_previsao')
    nome_arquivo += '.csv'
with col2:
    st.download_button('Download', data = gerar_conteudo_download(df_forecasting), file_name=nome_arquivo, mime = 'text/csv', on_click=mensagem_sucesso)

#Explicar a escolha do modelo
#Inserir o modelo Arima