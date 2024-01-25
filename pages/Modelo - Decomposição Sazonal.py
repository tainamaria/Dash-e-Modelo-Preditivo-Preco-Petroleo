import streamlit as st
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from utils import leitura_csv,decomposicao

st.set_page_config(page_title= 'Componentes de Decomposição - Preço dos Combustíveis', layout='wide', page_icon= ':fuelpump:')
st.title('Análise Sazonal 📊')

st.markdown('<p style="text-align: justify;"> Na decomposição sazonal de uma série temporal, os termos "multiplicativo" (multi) e "aditivo" (add) referem-se à maneira como os componentes de tendência e sazonalidade são combinados para reconstruir a série original.</p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Decomposição Aditiva:</span> Série temporal modelada como a soma dos componentes de tendência, sazonalidade e resíduos. Útil quando variação sazonal é aproximadamente constante ao longo do tempo.</p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Decomposição Multiplicativa:</span> Série temporal modelada como o produto dos componentes de tendência, sazonalidade e resíduos. Útil quando a variação sazonal muda proporcionalmente com o nível da série temporal.</p>', unsafe_allow_html = True)

## LEITURA DOS DADOS DO ARQUIVO GRAVADO
arquivo = 'dados_preco_petroleo.csv'
dados = leitura_csv(arquivo)

df_semanal = dados.resample('W')['Preco'].mean()
df_mensal = dados.resample('M')['Preco'].mean()

modelo = st.sidebar.selectbox("Selecione o modelo", ['Multiplicativo','Aditivo'])
formato = st.sidebar.selectbox("Selecione o formato", ['Diário','Semanal','Mensal'])

if (modelo == 'Multiplicativo' and formato == 'Diário'):
    st.markdown('<h2> Dados diários com decomposição multiplicativa </h2>', unsafe_allow_html = True)
    result_mult_diaria = seasonal_decompose(dados, period = 365, model='multiplicative')
    decomposicao(dados,result_mult_diaria)

elif (modelo == 'Aditivo' and formato == 'Diário'):
    st.markdown('<h2> Dados diários com decomposição aditiva </h2>', unsafe_allow_html = True)
    result_adit_diaria = seasonal_decompose(dados, period = 365, model='aditive')
    decomposicao(dados,result_adit_diaria)   

elif (modelo == 'Multiplicativo' and formato == 'Semanal'):
    st.markdown('<h2> Dados semanais com decomposição multiplicativa </h2>', unsafe_allow_html = True)
    result_adit_semanal = seasonal_decompose(df_semanal, period = 30, model='multiplicative')
    decomposicao(df_semanal,result_adit_semanal)   

elif (modelo == 'Aditivo' and formato == 'Semanal'):
    st.markdown('<h2> Dados semanais com decomposição aditiva </h2>', unsafe_allow_html = True)
    result_adit_semanal = seasonal_decompose(df_semanal, period = 30, model='aditive')
    decomposicao(df_semanal,result_adit_semanal)

elif (modelo == 'Multiplicativo' and formato == 'Mensal'):
    st.markdown('<h2> Dados mensais com decomposição multiplicativa </h2>', unsafe_allow_html = True)
    result_adit_mensal = seasonal_decompose(df_mensal, period = 30, model='multiplicative')
    decomposicao(df_mensal,result_adit_mensal)   

elif (modelo == 'Aditivo' and formato == 'Mensal'):
    st.markdown('<h2> Dados mensais com decomposição aditiva </h2>', unsafe_allow_html = True)
    result_adit_mensal = seasonal_decompose(df_mensal, period = 30, model='aditive')
    decomposicao(df_mensal,result_adit_mensal)


#Explicar o que é cada gráfico