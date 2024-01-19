## IMPORTAÇÃO ARQUIVOS
import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(page_title= 'Dashboard - Preço dos Combustíveis', layout='wide', page_icon= ':fuelpump:')
st.title('Dashboard - Variação do Preço do Petróleo :fuelpump:')

## DADOS
dados = pd.read_html('http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view', encoding='utf-8', decimal=',')
dados = dados[2]
dados.columns = dados.iloc[0]
dados = dados[1:]
dados = dados.rename(columns={'Preço - petróleo bruto - Brent (FOB)': 'Preco'})
dados['Data'] = pd.to_datetime(dados['Data'], format = '%d/%m/%Y')
dados.Preco = dados.Preco.astype(float)
dados.Preco = dados.Preco/100
dados = dados.set_index('Data')

## TABELAS


## GRÁFICOS
fig_linha_data = px.line(dados, 
                    x=dados.index, 
                    y=dados.columns[0], 
                    title='Linha do tempo', 
                    labels={'index': 'Ano', dados.columns[0]: 'Valor'})


## VISUALIZAÇÃO NO STREAMLIT
st.plotly_chart(fig_linha_data)

st.dataframe(dados.head(10))



