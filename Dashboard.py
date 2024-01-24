## IMPORTAÇÃO ARQUIVOS
import streamlit as st
import pandas as pd
import plotly.express as px
from funcoes import webscraping

st.set_page_config(page_title= 'Dashboard - Preço dos Combustíveis', layout='wide', page_icon= ':fuelpump:')
st.title('Dashboard - Variação do Preço do Petróleo :fuelpump:')

## LEITURA DOS DADOS NA WEB
dados = webscraping()

## TABELAS
menor_data = dados.index.min()
link_image = 'https://drive.google.com/drive/folders/10zGehcEkLUkTncPGBuabC-OMwCE70pvM?usp=sharing'

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
### Cartões
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric('Dados atualizados até:', dados.index.max().strftime('%d/%m/%Y')) 
with col2:
    st.metric('Dados monitorados desde:', dados.index.min().strftime('%d/%m/%Y')) 
with col3:
    st.metric('Menor preço histórico:', dados['Preco'].min())
with col4:
    st.metric('Menor preço histórico:', dados['Preco'].max())

### Gráficos
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_linha_data, use_container_width=True)
    st.plotly_chart(fig_picos_preco, use_container_width=True)
with col2:
    st.plotly_chart(fig_media_mensal_anos, use_container_width=True)
    st.plotly_chart(fig_vales_preco, use_container_width=True)    



