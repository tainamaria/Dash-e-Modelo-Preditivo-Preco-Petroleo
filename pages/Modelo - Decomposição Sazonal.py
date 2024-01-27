import streamlit as st
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from utils import leitura_csv,decomposicao

st.set_page_config(page_title= 'Modelo - Decomposição Sazonal', layout='wide', page_icon= ':fuelpump:')
st.title('Análise Sazonal 📊')

st.markdown('<p style="text-align: justify;"> Na decomposição sazonal de uma série temporal, os termos "multiplicativo" (multi) e "aditivo" (add) referem-se à maneira como os componentes de tendência e sazonalidade são combinados para reconstruir a série original.</p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Decomposição Aditiva:</span> Série temporal modelada como a soma dos componentes de tendência, sazonalidade e resíduos. Útil quando variação sazonal é aproximadamente constante ao longo do tempo.</p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Decomposição Multiplicativa:</span> Série temporal modelada como o produto dos componentes de tendência, sazonalidade e resíduos. Útil quando a variação sazonal muda proporcionalmente com o nível da série temporal.</p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"> Também é possível decompor os dados de acordo com o número de ciclos completos de sazonalidade (period), este parâmetro é importante porque ajuda a identificar padrões sazonais nos dados:</p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Sazonalidade diária:</span> dados diários definido com period=1.</p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Sazonalidade semanal:</span> dados diários definido period=7.</p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Sazonalidade mensal:</span> dados diários definido period=30.</p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Sazonalidade anual:</span> dados diários definido period=365.</p>', unsafe_allow_html = True)

## LEITURA DOS DADOS DO ARQUIVO GRAVADO
arquivo = 'dados_preco_petroleo.csv'
dados = leitura_csv(arquivo)

df_semanal = dados.resample('W')['Preco'].mean()
df_mensal = dados.resample('M')['Preco'].mean()

modelo = st.sidebar.selectbox("Selecione o modelo de decomposição", ['Multiplicativo','Aditivo'])
formato = st.sidebar.selectbox("Selecione o periodo de ciclos", ['1','7','30','365'])

if (modelo == 'Multiplicativo' and formato == '1'):
    st.markdown('<h2> Sazonalidade diária com decomposição multiplicativa </h2>', unsafe_allow_html = True)
    result_mult_diaria = seasonal_decompose(dados, period = 1, model='multiplicative')
    decomposicao(dados,result_mult_diaria)

elif (modelo == 'Aditivo' and formato == '1'):
    st.markdown('<h2> Sazonalidade diária com decomposição aditiva </h2>', unsafe_allow_html = True)
    result_adit_diaria = seasonal_decompose(dados, period = 1, model='aditive')
    decomposicao(dados,result_adit_diaria)   

elif (modelo == 'Multiplicativo' and formato == '7'):
    st.markdown('<h2> Sazonalidade semanal com decomposição multiplicativa </h2>', unsafe_allow_html = True)
    result_mult_diaria = seasonal_decompose(dados, period = 7, model='multiplicative')
    decomposicao(dados,result_mult_diaria)

elif (modelo == 'Aditivo' and formato == '7'):
    st.markdown('<h2> Sazonalidade semanal com decomposição aditiva </h2>', unsafe_allow_html = True)
    result_adit_diaria = seasonal_decompose(dados, period = 7, model='aditive')
    decomposicao(dados,result_adit_diaria) 

elif (modelo == 'Multiplicativo' and formato == '30'):
    st.markdown('<h2> Sazonalidade mensal com decomposição multiplicativa </h2>', unsafe_allow_html = True)
    result_mult_diaria = seasonal_decompose(dados, period = 30, model='multiplicative')
    decomposicao(dados,result_mult_diaria)

elif (modelo == 'Aditivo' and formato == '30'):
    st.markdown('<h2> Sazonalidade mensal com decomposição aditiva </h2>', unsafe_allow_html = True)
    result_adit_diaria = seasonal_decompose(dados, period = 30, model='aditive')
    decomposicao(dados,result_adit_diaria) 

elif (modelo == 'Multiplicativo' and formato == '365'):
    st.markdown('<h2> Sazonalidade anual com decomposição multiplicativa </h2>', unsafe_allow_html = True)
    result_mult_diaria = seasonal_decompose(dados, period = 365, model='multiplicative')
    decomposicao(dados,result_mult_diaria)

elif (modelo == 'Aditivo' and formato == '365'):
    st.markdown('<h2> Sazonalidade anual com decomposição aditiva </h2>', unsafe_allow_html = True)
    result_adit_diaria = seasonal_decompose(dados, period = 365, model='aditive')
    decomposicao(dados,result_adit_diaria) 

#Explicar o que é cada gráfico