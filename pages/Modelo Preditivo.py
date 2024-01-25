## IMPORTAÇÃO ARQUIVOS
import streamlit as st
from datetime import date
import pandas as pd
from utils import leitura_csv,modelo_ets,graf_comparativo,dias_uteis_futuros,colunas_ets,gerar_conteudo_download
import time

st.set_page_config(page_title= 'Modelo Preditivo - Preço dos Combustíveis', layout='wide', page_icon= ':fuelpump:')
st.title('Modelo Preditivo :telescope:')

st.markdown('<p style="text-align: justify;">ARIMA (AutoRegressive Integrated Moving Average) e ETS (Error-Trend-Seasonality) são modelos de séries temporais usados para prever valores futuros com base em padrões identificados nos dados históricos.</p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">ARIMA:</span> Modela a série temporal com base em componentes autoregressivos, diferenciação e médias móveis. Eficaz para dados estacionários ou que podem ser tornados estacionários através de diferenciação. Pode capturar tendências e padrões sazonais. </p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">ETS:</span> Modela a série temporal em termos de erro, tendência e sazonalidade. Inclui componentes aditivos e multiplicativos, dependendo da natureza da série. É mais flexível e lida bem com padrões não lineares.</p>', unsafe_allow_html = True)


algoritmo = st.sidebar.selectbox("Selecione o algoritmo", ['ETS','ARIMA'])
data_inicial = st.sidebar.date_input('Data inicial', date.today())
qtd_dias_previsao = st.sidebar.number_input("Escolha a quantidade de dias que deseja prever", min_value=0, max_value=365, value=30)
botao_clicado = st.sidebar.button("Aplicar", key="botao1", help="Botão para aplicar no modelo de treino a partir da data selecionada")

## LEITURA DOS DADOS DO ARQUIVO GRAVADO
arquivo = 'dados_preco_petroleo.csv'
dados = leitura_csv(arquivo)

if algoritmo == 'ETS':
    st.header('ETS - Error Tren Seasonality')
    if botao_clicado:
        # dados_selecionados = dados[dados.index >= data_inicial.astype(datetime.date)]
        melhor_mae, melhores_parametros, melhores_dados_teste, melhores_dados_treinamento, fit_train = modelo_ets(dados, 365)
        colunas_ets(melhores_dados_teste,melhores_dados_treinamento,melhor_mae,melhores_parametros)
    else:
        with st.spinner("Processando..."):
            melhor_mae, melhores_parametros, melhores_dados_teste, melhores_dados_treinamento, fit_train = modelo_ets(dados,365)
            colunas_ets(melhores_dados_teste,melhores_dados_treinamento,melhor_mae,melhores_parametros)

    dias_futuros = dias_uteis_futuros(dados.index.max(),90)
    
    figura = graf_comparativo(dados.index.to_numpy(),dados['Preco'].to_numpy(),melhores_dados_teste.index.to_numpy(),fit_train.forecast(len(melhores_dados_teste)).to_numpy(),dias_futuros,fit_train.forecast(90).to_numpy(),'Dados históricos x Previsões')

st.plotly_chart(figura, use_container_width=True)

df_forecasting = pd.DataFrame()
df_forecasting['Data'] = dias_futuros
df_forecasting['Preco'] = fit_train.forecast(90).reset_index(drop=True)

button = st.download_button(
label="Baixar Dados Previstos em CSV",
data=gerar_conteudo_download(df_forecasting),
key="download_button")

#Trocar a data para barra em vez de hifen igual no Dashboard
#Colocar as datas previstas com valores de pico
#Explicar a escolha do modelo
#Inserir o modelo Arima