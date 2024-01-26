# Importação das bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils import webscraping,graf_marcado_max_min

#Configuração da página
st.set_page_config(page_title= 'Dashboard - Preço do Petróleo', layout='wide', page_icon= ':fuelpump:')
st.title('Dashboard - Variação do Preço do Petróleo :fuelpump:')

# Webscraping
url = 'http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view'
coluna = 'Preco'
dados = webscraping(url,coluna)

# Construção dos dataframes 
dados_sem_dataindex = dados.reset_index()
dados_sem_dataindex['Ano'] = dados_sem_dataindex['Data'].dt.year.astype(int)

media_mensal_anos = dados.groupby(pd.Grouper(freq= 'M'))[['Preco']].mean().reset_index() #Agrupando os dados por mês
media_mensal_anos['Ano'] = media_mensal_anos['Data'].dt.year.astype(int)
media_mensal_anos['Mes'] = media_mensal_anos['Data'].dt.month_name()

picos_preco = media_mensal_anos.set_index('Data').sort_values('Preco', ascending=False).head(10)

vales_preco = media_mensal_anos.set_index('Data').sort_values('Preco', ascending=True).head(10)

# Construção dos gráficos          
fig_picos_preco = px.bar(picos_preco,
                        x = picos_preco['Mes'].astype(str) + '/' + picos_preco['Ano'].astype(str),
                        y = 'Preco',
                        text_auto=True,
                        title= f'Top 10 meses com média de preços mais altos')
fig_picos_preco.update_xaxes(type='category')
fig_picos_preco.update_layout(xaxis_title= 'Data', yaxis_title = 'Preço (US$)')

fig_vales_preco = px.bar(vales_preco,
                        x = vales_preco['Mes'].astype(str) + '/' + vales_preco['Ano'].astype(str),
                        y = 'Preco',
                        text_auto=True,
                        title= f'Top 10 meses com média de preços mais baixos')
fig_vales_preco.update_xaxes(type='category')
fig_vales_preco.update_layout(xaxis_title= 'Data', yaxis_title = 'Preço (US$)')


# Visualização dos visuais no Streamlit
## Cartões
cor_estilizada = 'color: #0145AC;'
fonte_negrito = 'font-weight: bold;'

col1, col2, col3, col4 = st.columns(4)
with col1:
    metrica1 = dados.index.max().strftime('%d/%m/%Y')
    st.markdown(f"<h2 style='{cor_estilizada}'>{metrica1}</h2> <span style='{fonte_negrito}'> Dados atualizados até </span>", unsafe_allow_html=True)
    #st.metric('Dados atualizados até:', value=dados.index.max().strftime('%d/%m/%Y')) 
with col2: 
    metrica2 = dados.index.min().strftime('%d/%m/%Y')
    st.markdown(f"<h2 style='{cor_estilizada}'> {metrica2} </h2> <span style='{fonte_negrito}'> Dados monitorados desde</span> ", unsafe_allow_html=True) 
with col3:
    metrica3 = dados['Preco'].min()
    data_metrica3 = dados[dados['Preco']==dados['Preco'].min()].index
    st.markdown(f"<h2 style='{cor_estilizada}'> US$ {metrica3:.2f} </h2> <span style='{fonte_negrito}'> Menor preço histórico <br> (atingido em  {data_metrica3[0].strftime('%d/%m/%Y')})</span> ", unsafe_allow_html=True) 
    #st.metric('Menor preço histórico:', value=dados['Preco'].min().round(2))
with col4:
    metrica4 = dados['Preco'].max()
    data_metrica4 = dados[dados['Preco']==dados['Preco'].max()].index
    st.markdown(f"<h2 style='{cor_estilizada}'> US$ {metrica4:.2f} </h2> <span style='{fonte_negrito}'> Maior preço histórico <br> (atingido em  {data_metrica4[0].strftime('%d/%m/%Y')})</span> ", unsafe_allow_html=True)

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

## Gráficos
data = st.slider('Selecione o intervalo', min_value=media_mensal_anos['Ano'].min(), max_value=media_mensal_anos['Ano'].max(), value=(2019, media_mensal_anos['Ano'].max()))
col1, col2 = st.columns(2)
with col1:
    dados_intervalo = dados_sem_dataindex.query('@data[0] <= Ano <= @data[1]')
    st.plotly_chart(graf_marcado_max_min(dados_intervalo), use_container_width=True)
    st.divider()
    st.plotly_chart(fig_picos_preco, use_container_width=True)
with col2:
    fig_media_mensal_anos = px.line(media_mensal_anos.query('@data[0] <= Ano <= @data[1]'), 
                             x = 'Mes',
                             y = 'Preco',
                             markers = True,
                             range_y = (0, media_mensal_anos.max()),
                             color = 'Ano',
                             line_dash = 'Ano',
                             title = 'Média de preço por mês e ano')
    fig_media_mensal_anos.update_layout(yaxis_title = 'Média de Preço (US$)')
    st.plotly_chart(fig_media_mensal_anos, use_container_width=True)
    st.divider()
    st.plotly_chart(fig_vales_preco, use_container_width=True)    


#ESTRESSAR todos os filtros em TODAS AS PÁGINAS - ******** PENDENTE ********

    

