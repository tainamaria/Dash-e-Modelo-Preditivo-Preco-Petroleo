import streamlit as st

st.set_page_config(page_title= 'Dashboard - Preço dos Combustíveis', layout='wide', page_icon= ':fuelpump:')

### Insights
st.write('## Insights')
st.image('img/img_pontos_historicos.JPG', caption='Histórico de preços')

#Altas
st.markdown('<h3> Principais fatos históricos que afetaram os preços </h3>', unsafe_allow_html = True)

st.markdown('<p style="text-align: justify;"><span style="color:#ED7D31; font-weight: bold">Julho/2008:</span> o fato que culmina no pico de preço do barril de petróleo nesse período, vem acompanhado de uma curva crescente desde o ano de 2004, com instabilidade geopolítica, crescimento da demanda global, especulação no mercado financeiro. Em 2005, por exemplo, o evento climático do furacão Katrina causou danos significativos às instalações de produção de petróleo e gás no Golfo do México, afetando a oferta. Tensões geopolíticas em regiões chave de produção de petróleo, como o Oriente Médio, também contribuíram para a preocupação com a segurança no fornecimento. Eventos como a tensão entre os Estados Unidos e o Irã, assim como conflitos em regiões produtoras, geraram incertezas que influenciaram nos crescentes preços do petróleo.</p>', unsafe_allow_html = True)

st.markdown('<p style="text-align: justify;"> <span style="color:#70AD47; font-weight: bold">Janeiro/2009:</span> a recessão causada pela crise financeira global ocorrida em 2008 e conhecida como "subprime" foi a grande causadora da queda abrupta do preço do petróleo nesse período. A crise, ocasionada pelo estouro da bolha imobiliária nos Estados Unidos, levou principalmente os próprios EUA e a Europa a uma profunda recessão derrubando a demanda por petróleo e, consequentemente, seu preço.</p>', unsafe_allow_html = True)

st.markdown('<p style="text-align: justify;"> <span style="color:#ED7D31; font-weight: bold">Maio/2011:</span>  Após a crise do subprime em 2008, diversas economias globais começaram a se recuperar, resultando em um aumento na demanda por energia, especialmente nos países em desenvolvimento. Além disso, eventos geopolíticos, como instabilidades no Oriente Médio e conflitos em importantes regiões produtoras de petróleo, geraram preocupações sobre a segurança no fornecimento, impactando os preços do petróleo. A desvalorização contínua do dólar americano também desempenhou um papel, tornando o petróleo mais caro para compradores que utilizavam outras moedas. Essa combinação de fatores contribuiu para a retomada da trajetória de alta nos preços dos combustíveis durante o período mencionado, culminando em maio de 2011 </p>', unsafe_allow_html = True) 

#TIRAR MARÇO DE 2012 NA IMAGEM

st.markdown('<p style="text-align: justify;"> <span style="color:#70AD47; font-weight: bold">Janeiro/2016:</span>  A queda nos preços do barril de petróleo de julho de 2014 a janeiro de 2016 foi principalmente impulsionada por um excesso de oferta global combinado com uma desaceleração da demanda. A produção de petróleo de xisto nos Estados Unidos aumentou significativamente, tornando o país menos dependente das importações e contribuindo para o aumento da oferta global. Paralelamente, a Organização dos Países Exportadores de Petróleo (OPEP) manteve elevados níveis de produção, em parte para preservar sua participação de mercado em meio à crescente produção de xisto. No entanto, a desaceleração econômica global, especialmente na China, reduziu a demanda por petróleo. O excesso de oferta, combinado com a falta de coordenação entre os principais produtores para reduzir a produção, levou a uma queda acentuada nos preços do petróleo, atingindo seu ponto mais baixo em janeiro de 2016. </p>', unsafe_allow_html = True)

st.markdown('<p style="text-align: justify;"> <span style="color:#70AD47; font-weight: bold">Abril/2020:</span>  A queda abrupta nos preços do barril de petróleo de janeiro a março de 2020 foi amplamente influenciada pela combinação de eventos relacionados à pandemia de COVID-19 e uma guerra de preços entre a Arábia Saudita e a Rússia. A disseminação global do coronavírus resultou em medidas de confinamento e restrições de viagem, reduzindo drasticamente a demanda por petróleo, pois indústrias pararam, viagens diminuíram e a atividade econômica foi significativamente afetada. Em meio a esse cenário, a Arábia Saudita e a Rússia discordaram sobre os cortes na produção para sustentar os preços do petróleo em face da demanda reduzida. Isso levou a uma guerra de preços em que ambos os países aumentaram sua produção, inundando ainda mais o mercado com petróleo em um momento de queda acentuada na demanda </p>', unsafe_allow_html = True)

st.markdown('<p style="text-align: justify;"> <span style="color:#ED7D31; font-weight: bold">Março/2022:</span>  xpto xptoxpto xptoxpto xptoxpto xptoxpto xptoxpto xpto </p>', unsafe_allow_html = True) 

#TIRAR JUNHO DE 2022 NA IMAGEM  

#AVALIAR COLOCAR O GRÁFICO COM O DÓLAR COMERCIAL HISTÓRICO JA QUE ELE E UM DOS PRINCIPAIS FATORES DA VRIAÇÃO DE PRECOS