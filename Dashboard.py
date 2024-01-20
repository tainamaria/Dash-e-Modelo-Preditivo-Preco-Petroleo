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
media_mensal_anos = dados.groupby(pd.Grouper(freq= 'M'))[['Preco']].mean().reset_index() #Agrupando os dados por mês
media_mensal_anos['Ano'] = media_mensal_anos['Data'].dt.year.astype(int)
media_mensal_anos['Mes'] = media_mensal_anos['Data'].dt.month_name()

picos_preco = media_mensal_anos.set_index('Data').sort_values('Preco', ascending=False).head(10)

vales_preco = media_mensal_anos.set_index('Data').sort_values('Preco', ascending=True).head(10)

## GRÁFICOS
fig_linha_data = px.line(dados, 
                    x=dados.index, 
                    y=dados.columns[0], 
                    title='Linha do tempo', 
                    labels={'index': 'Ano', dados.columns[0]: 'Valor'})
fig_linha_data.update_layout(yaxis_title = 'Preço')

fig_media_mensal_anos = px.line(media_mensal_anos,
                             x = 'Mes',
                             y = 'Preco',
                             markers = True,
                             range_y = (0, media_mensal_anos.max()),
                             color = 'Ano',
                             line_dash = 'Ano',
                             title = 'Média de preço por mês e ano')
fig_media_mensal_anos.update_layout(yaxis_title = 'Média de Preço')
            
fig_picos_preco = px.bar(picos_preco,
                        x = picos_preco['Mes'].astype(str) + '/' + picos_preco['Ano'].astype(str),
                        y = 'Preco',
                        text_auto=True,
                        title= f'Top 10 preços mais altos histórico')
fig_picos_preco.update_xaxes(type='category')
fig_picos_preco.update_layout(xaxis_title= 'Data', yaxis_title = 'Preço')

fig_vales_preco = px.bar(vales_preco,
                        x = vales_preco['Mes'].astype(str) + '/' + vales_preco['Ano'].astype(str),
                        y = 'Preco',
                        text_auto=True,
                        title= f'Top 10 preços mais baixos histórico')
fig_vales_preco.update_xaxes(type='category')
fig_vales_preco.update_layout(xaxis_title= 'Data', yaxis_title = 'Preço')




## VISUALIZAÇÃO NO STREAMLIT
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_linha_data)
    st.plotly_chart(fig_picos_preco)
with col2:
    st.plotly_chart(fig_media_mensal_anos)
    st.plotly_chart(fig_vales_preco)    
    

st.dataframe(dados.head(20))

st.dataframe(media_mensal_anos.head(20))

st.dataframe(picos_preco)
#gráfico comparando os preços médios por mês e ano (semelhante ao do projeto da Alura) - OK
#gráfico mostrando as datas que houve pico de preço e o preço - OK
#gráfico mostrando as datas que houve preço mais baixo e o preço - OK


