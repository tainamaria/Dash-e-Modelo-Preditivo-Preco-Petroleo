import pickle
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Modelo ETS para previsão dos dias, utilizando qtd de dias recentes para treinamento, qtd de dias que deseja prever e, os parâmetros de tendência e sazonalidade
def modelo_ets_previsao(dados, qt_dias_historico, qt_dias_prever, trend, seasonal):
    dados = dados.tail(qt_dias_historico)
  
    # Criando o modelo ETS
    modelo_ets = ExponentialSmoothing(dados['Preco'], trend=trend, seasonal=seasonal, seasonal_periods=30)
    
    # Treinando o modelo
    resultado = modelo_ets.fit()

    # Fazendo previsões
    previsao = resultado.forecast(steps=qt_dias_prever)

    return previsao

# Salvar a função usando pickle
with open('modelo_ets.pkl', 'wb') as arquivo:
    pickle.dump(modelo_ets_previsao, arquivo)
