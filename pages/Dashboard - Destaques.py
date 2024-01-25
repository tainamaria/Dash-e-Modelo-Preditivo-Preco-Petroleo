import streamlit as st
import pandas as pd
from utils import leitura_csv,webscraping,graf_dois_eixos

st.set_page_config(page_title= 'Dashboard - Preço dos Combustíveis', layout='wide', page_icon= ':fuelpump:')
### Insights
st.write('## Destaques 🕵️‍♀️')

with st.spinner("Processando..."):
    url = 'http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=38590&module=M'
    coluna = 'Taxa'
    dados_taxa = webscraping(url,coluna)

    arquivo = 'dados_preco_petroleo.csv'
    dados_preco = leitura_csv(arquivo)

    df_merged = pd.merge(dados_preco, dados_taxa, left_index=True, right_index=True, how='inner')
    df_merged.Taxa = df_merged.Taxa/100

    x = df_merged.index
    y1 = df_merged.Preco
    y2 = df_merged.Taxa

col1, col2 = st.columns(2)
with col1:
    st.image('img/img_pontos_historicos.JPG', caption='Histórico de preços')
with col2:
    st.plotly_chart(graf_dois_eixos(x,y1,y2), use_container_width=True)

#Altas
st.markdown('<h3> Principais fatos históricos que afetaram os preços </h3>', unsafe_allow_html = True)

st.markdown('<p style="text-align: justify;"><span style="color:#ED7D31; font-weight: bold">Julho/2008:</span> o fato que culmina no pico de preço do barril de petróleo nesse período, vem acompanhado de uma curva crescente desde o ano de 2004, com instabilidade geopolítica, crescimento da demanda global, especulação no mercado financeiro. Em 2005, por exemplo, o evento climático do furacão Katrina causou danos significativos às instalações de produção de petróleo e gás no Golfo do México, afetando a oferta. Tensões geopolíticas em regiões chave de produção de petróleo, como o Oriente Médio, também contribuíram para a preocupação com a segurança no fornecimento. Eventos como a tensão entre os Estados Unidos e o Irã, assim como conflitos em regiões produtoras, geraram incertezas que influenciaram nos crescentes preços do petróleo.</p>', unsafe_allow_html = True)

st.markdown('<p style="text-align: justify;"> <span style="color:#70AD47; font-weight: bold">Janeiro/2009:</span> a recessão causada pela crise financeira global ocorrida em 2008 e conhecida como "subprime" foi a grande causadora da queda abrupta do preço do petróleo nesse período. A crise, ocasionada pelo estouro da bolha imobiliária nos Estados Unidos, levou principalmente os próprios EUA e a Europa a uma profunda recessão derrubando a demanda por petróleo e, consequentemente, seu preço.</p>', unsafe_allow_html = True)

st.markdown('<p style="text-align: justify;"> <span style="color:#ED7D31; font-weight: bold">Maio/2011:</span>  Após a crise do subprime em 2008, diversas economias globais começaram a se recuperar, resultando em um aumento na demanda por energia, especialmente nos países em desenvolvimento. Além disso, eventos geopolíticos, como instabilidades no Oriente Médio e conflitos em importantes regiões produtoras de petróleo, geraram preocupações sobre a segurança no fornecimento, impactando os preços do petróleo. A desvalorização contínua do dólar americano também desempenhou um papel, tornando o petróleo mais caro para compradores que utilizavam outras moedas. Essa combinação de fatores contribuiu para a retomada da trajetória de alta nos preços dos combustíveis durante o período mencionado, culminando em maio de 2011 </p>', unsafe_allow_html = True) 

st.markdown('<p style="text-align: justify;"> <span style="color:#70AD47; font-weight: bold">Janeiro/2016:</span>  A queda nos preços do barril de petróleo de julho de 2014 a janeiro de 2016 foi principalmente impulsionada por um excesso de oferta global combinado com uma desaceleração da demanda. A produção de petróleo de xisto nos Estados Unidos aumentou significativamente, tornando o país menos dependente das importações e contribuindo para o aumento da oferta global. Paralelamente, a Organização dos Países Exportadores de Petróleo (OPEP) manteve elevados níveis de produção, em parte para preservar sua participação de mercado em meio à crescente produção de xisto. No entanto, a desaceleração econômica global, especialmente na China, reduziu a demanda por petróleo. O excesso de oferta, combinado com a falta de coordenação entre os principais produtores para reduzir a produção, levou a uma queda acentuada nos preços do petróleo, atingindo seu ponto mais baixo em janeiro de 2016. </p>', unsafe_allow_html = True)

st.markdown('<p style="text-align: justify;"> <span style="color:#70AD47; font-weight: bold">Abril/2020:</span>  A queda abrupta nos preços do barril de petróleo de janeiro a março de 2020 foi amplamente influenciada pela combinação de eventos relacionados à pandemia de COVID-19 e uma guerra de preços entre a Arábia Saudita e a Rússia. A disseminação global do coronavírus resultou em medidas de confinamento e restrições de viagem, reduzindo drasticamente a demanda por petróleo, pois indústrias pararam, viagens diminuíram e a atividade econômica foi significativamente afetada. Em meio a esse cenário, a Arábia Saudita e a Rússia discordaram sobre os cortes na produção para sustentar os preços do petróleo em face da demanda reduzida. Isso levou a uma guerra de preços em que ambos os países aumentaram sua produção, inundando ainda mais o mercado com petróleo em um momento de queda acentuada na demanda </p>', unsafe_allow_html = True)

st.markdown('<p style="text-align: justify;"> <span style="color:#ED7D31; font-weight: bold">Março/2022:</span>  As medidas de contenção da pandemia foram gradualmente relaxadas, impulsionando a demanda por energia à medida que as atividades econômicas se recuperavam. Além disso, a implementação de campanhas de vacinação contra a COVID-19 em vários países melhorou as perspectivas para a recuperação econômica global, contribuindo para a confiança dos investidores nos mercados de commodities. Paralelamente, importantes produtores de petróleo, incluindo membros da OPEP e aliados, como a Rússia, ajustaram a produção, concordando em cortes coordenados para equilibrar a oferta e demanda. </p>', unsafe_allow_html = True) 

#Cortar a imagem para encaixar melhor (selecionar no plotly depois refazer os pontos no ppt)
