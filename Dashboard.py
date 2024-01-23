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

### Insights
st.write('## Insights')
st.image('img/img_pontos_historicos.JPG', caption='Histórico de preços')

#Altas
st.markdown('<h3> Principais fatos históricos que afetaram os preços </h3>', unsafe_allow_html = True)
st.markdown('<p><span style="color:#ED7D31; font-weight: bold">Julho/2008:</span> o fato que culmina no pico de preço do barril de petróleo nesse período, vem acompanhado de uma curva crescente desde o ano de 2004, com instabilidade geopolítica, crescimento da demanda global, especulação no mercado financeiro. Em 2005, por exemplo, o evento climático do furacão Katrina causou danos significativos às instalações de produção de petróleo e gás no Golfo do México, afetando a oferta. Tensões geopolíticas em regiões chave de produção de petróleo, como o Oriente Médio, também contribuíram para a preocupação com a segurança no fornecimento. Eventos como a tensão entre os Estados Unidos e o Irã, assim como conflitos em regiões produtoras, geraram incertezas que influenciaram nos crescentes preços do petróleo.</p>', unsafe_allow_html = True)
st.markdown('<p> <span style="color:#70AD47; font-weight: bold">Janeiro/2009:</span> a recessão causada pela crise financeira global ocorrida em 2008 e conhecida como "subprime" foi a grande causadora da queda abrupta do preço do petróleo nesse período. A crise, ocasionada pelo estouro da bolha imobiliária nos Estados Unidos, levou principalmente os próprios EUA e a Europa a uma profunda recessão derrubando a demanda por petróleo e, consequentemente, seu preço.</p>', unsafe_allow_html = True)
st.markdown('<p> <span style="color:#ED7D31; font-weight: bold">Maio/2011:</span>  xpto xptoxpto xptoxpto xptoxpto xptoxpto xptoxpto xpto </p>', unsafe_allow_html = True) 
st.markdown('<p> <span style="color:#ED7D31; font-weight: bold">Março/2012:</span>  xpto xptoxpto xptoxpto xptoxpto xptoxpto xptoxpto xpto </p>', unsafe_allow_html = True) 
st.markdown('<p> <span style="color:#70AD47; font-weight: bold">Janeiro/2016:</span>  xpto xptoxpto xptoxpto xptoxpto xptoxpto xptoxpto xpto </p>', unsafe_allow_html = True)
st.markdown('<p> <span style="color:#70AD47; font-weight: bold">Abril/2020:</span>  xpto xptoxpto xptoxpto xptoxpto xptoxpto xptoxpto xpto </p>', unsafe_allow_html = True)
st.markdown('<p> <span style="color:#ED7D31; font-weight: bold">Março/2022:</span>  xpto xptoxpto xptoxpto xptoxpto xptoxpto xptoxpto xpto </p>', unsafe_allow_html = True) 
st.markdown('<p> <span style="color:#ED7D31; font-weight: bold">Junho/2022:</span>  xpto xptoxpto xptoxpto xptoxpto xptoxpto xptoxpto xpto </p>', unsafe_allow_html = True)  


st.dataframe(dados.head(20))
st.metric('linhas dados',dados.shape[0])

st.dataframe(media_mensal_anos.head(20))
st.metric('linhas media_mensal',media_mensal_anos.shape[0])

st.dataframe(picos_preco)
#gráfico comparando os preços médios por mês e ano (semelhante ao do projeto da Alura) - OK
#gráfico mostrando as datas que houve pico de preço e o preço - OK
#gráfico mostrando as datas que houve preço mais baixo e o preço - OK
#Cartões com:
#Maior preço histórico, menor preço, desde quando é medido - OK
#publicar - 
#dar uma olhada nos filtros que a Tainá tá fazendo pra ver se acho o pq não tá funcionando
#Alimentar pág Desenvolvimento


