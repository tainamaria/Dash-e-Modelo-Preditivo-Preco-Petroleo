## IMPORTAÇÃO ARQUIVOS
import streamlit as st
import pandas as pd
from utils import leitura_csv,modelo_ets,graf_comparativo,dias_uteis_futuros,colunas_ets,gerar_conteudo_download,mensagem_sucesso

st.set_page_config(page_title= 'Modelo - Predição', layout='wide', page_icon= ':fuelpump:')
st.title('Modelo Preditivo :telescope:')

st.markdown('<p style="text-align: justify;">ARIMA (AutoRegressive Integrated Moving Average) e ETS (Error-Trend-Seasonality) são modelos de séries temporais usados para prever valores futuros com base em padrões identificados nos dados históricos.</p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">ARIMA:</span> Modela a série temporal com base em componentes autoregressivos, diferenciação e médias móveis. Eficaz para dados estacionários ou que podem ser tornados estacionários através de diferenciação. Pode capturar tendências e padrões sazonais. </p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">ETS:</span> Modela a série temporal em termos de erro, tendência e sazonalidade. Inclui componentes aditivos e multiplicativos, dependendo da natureza da série. É mais flexível e lida bem com padrões não lineares.</p>', unsafe_allow_html = True)


algoritmo = st.sidebar.selectbox("Selecione o algoritmo", ['ETS','ARIMA'])

## LEITURA DOS DADOS DO ARQUIVO GRAVADO
arquivo = 'dados_preco_petroleo.csv'
dados = leitura_csv(arquivo)

qt_dias_previsao = 30

if algoritmo == 'ETS':
    st.header('ETS - Error Tren Seasonality')
    melhor_mae, melhores_parametros, melhores_dados_teste, melhores_dados_treinamento, fit_train = modelo_ets(dados,365)
    
    df_forecasting = pd.DataFrame()
    dias_futuros = dias_uteis_futuros(dados.index.max(),qt_dias_previsao)
    df_forecasting['Data'] = dias_futuros
    df_forecasting['Preco'] = fit_train.forecast(qt_dias_previsao).reset_index(drop=True)
    
    colunas_ets(melhores_dados_teste,melhores_dados_treinamento,melhor_mae,melhores_parametros,df_forecasting,qt_dias_previsao)

    figura = graf_comparativo(dados.tail(365).index.to_numpy(),dados.tail(365)['Preco'].to_numpy(),melhores_dados_teste.index.to_numpy(),fit_train.forecast(len(melhores_dados_teste)).to_numpy(),dias_futuros,fit_train.forecast(qt_dias_previsao).to_numpy(),'Dados históricos x Previsões')

    st.plotly_chart(figura, use_container_width=True)


elif algoritmo == 'ARIMA':
    st.header('ARIMA - Média Móvel Integrada Autoregressiva')
    st.markdown('<p style="text-align: justify;"> Para esse modelo foi utilizado o auto_arima, uma função do pacote Python pmdarima (também conhecido como pyramid-arima) que automatiza o processo de seleção do melhor modelo ARIMA para uma série temporal. Ele ajusta vários modelos ARIMA com diferentes combinações de parâmetros p, d e q (ordens do modelo ARIMA).</p>', unsafe_allow_html = True)
    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">p:</span> é a ordem do modelo autoregressivo; Mais especificamente é quantidade de lags(quantidade de valores correlacionados). </p>', unsafe_allow_html = True)
    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">d:</span> o número de vezes que as observações serão diferenciadas. </p>', unsafe_allow_html = True)
    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">q:</span> é a ordem do modelo de média móvel.</p>', unsafe_allow_html = True)

    # melhor_mae, dados_teste, dados_treino, modelo_arima_teste, modelo_arima = modelo_arima(dados,qt_dias_previsao)
    
    # df_forecasting = pd.DataFrame()
    # dias_futuros = dias_uteis_futuros(dados.index.max(),qt_dias_previsao)
    # df_forecasting['Data'] = dias_futuros
    # df_forecasting['Preco'] = modelo_arima.predict(n_periods=qt_dias_previsao).reset_index(drop=True)
    
    # colunas_arima(melhor_mae, dados_teste, dados_treino, modelo_arima_teste, df_forecasting, qt_dias_previsao)

    # figura = graf_comparativo(dados.tail(365).index.to_numpy(),dados.tail(365)['Preco'].to_numpy(),dados_teste.index.to_numpy(),modelo_arima_teste.predict(n_periods=len(dados_treino)).to_numpy(),dias_futuros,modelo_arima.predict(n_periods=qt_dias_previsao).to_numpy(),'Dados históricos x Previsões')

    # st.plotly_chart(figura, use_container_width=True)

st.markdown('Escreva um nome para o arquivo:')
col1, col2 = st.columns(2)
with col1:
    nome_arquivo = st.text_input('', label_visibility='collapsed', value='dados_previsao')
    nome_arquivo += '.csv'
with col2:
    st.download_button('Download', data = gerar_conteudo_download(df_forecasting), file_name=nome_arquivo, mime = 'text/csv', on_click=mensagem_sucesso)

#Explicar a escolha do modelo
#Inserir o modelo Arima