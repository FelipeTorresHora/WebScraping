import pandas as pd
from prophet import Prophet
from sklearn.metrics import r2_score, mean_absolute_error
import numpy as np
import matplotlib.pyplot as plt

def prever_preco_prophet(df_historical, days_futuro=30):
    # Preparar dados para o Prophet
    df_prophet = df_historical.rename(columns={'date': 'ds', 'price': 'y'})
    
    # Criar e treinar modelo
    modelo = Prophet(daily_seasonality=True, yearly_seasonality=False, weekly_seasonality=True)
    modelo.fit(df_prophet)
    
    # Gerar previsões
    future = modelo.make_future_dataframe(periods=days_futuro)
    forecast = modelo.predict(future)
    
    # Calcular métricas
    y_true = df_prophet['y'].values
    y_pred = forecast['yhat'][:-days_futuro].values
    
    return {
        'forecast': forecast,
        'modelo': modelo,
        'r2': r2_score(y_true, y_pred),
        'mae': mean_absolute_error(y_true, y_pred),
        'ultima_previsao': forecast['yhat'].values[-1]
    }

if __name__ == "__main__":
    # Dados de exemplo para teste
    dates = pd.date_range(start="2023-01-01", periods=90)
    np.random.seed(42)
    prices = 100 + np.cumsum(np.random.normal(0, 1, 90))  # Simulação de preços
    
    df_teste = pd.DataFrame({
        'date': dates,
        'price': prices
    })
    
    resultados = prever_preco_prophet(df_teste)
    
    print("=== Resultados do Modelo Prophet ===")
    print(f"R²: {resultados['r2']:.4f}")
    print(f"MAE: {resultados['mae']:.4f} R$")
    print(f"Previsão de preço para 30 dias: R$ {resultados['ultima_previsao']:.2f}")
    
    # Plotar resultados
    fig1 = resultados['modelo'].plot(resultados['forecast'])
    plt.title("Previsão do Preço")
    plt.show()
    
    fig2 = resultados['modelo'].plot_components(resultados['forecast'])
    plt.show()