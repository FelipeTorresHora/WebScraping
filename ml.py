import pandas as pd
from prophet import Prophet
from sklearn.metrics import r2_score, mean_absolute_error

def prever_preco_prophet(df_historical, days_futuro=30, window=5):
    try:
        # Verificar se df_historical tem os dados necessários
        if 'price' not in df_historical.columns or 'date' not in df_historical.columns:
            raise ValueError("O DataFrame deve conter as colunas 'price' e 'date'.")
        
        # Garantir que a coluna 'date' seja do tipo datetime
        df_historical['date'] = pd.to_datetime(df_historical['date'])
        
        # Filtrar apenas dias úteis (segunda a sexta)
        df_historical = df_historical[df_historical['date'].dt.weekday < 5].copy()
        
        if df_historical.empty:
            raise ValueError("Nenhum dado disponível após filtrar finais de semana.")
        
        # Suavizar os preços com média móvel
        df_historical['price_smooth'] = df_historical['price'].rolling(window=window, min_periods=1).mean()
        
        # Preparar dados para o Prophet
        df_prophet = df_historical.rename(columns={'date': 'ds', 'price_smooth': 'y'}).dropna()
        
        if df_prophet.empty:
            raise ValueError("Os dados preparados para o Prophet estão vazios após a suavização.")
        
        # Criar e treinar modelo com ajustes para reduzir oscilações
        modelo = Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=False,
            changepoint_prior_scale=0.05
        )
        modelo.fit(df_prophet)
        
        # Usar datas históricas exatas e adicionar dias úteis futuros
        historical_dates = df_prophet['ds'].tolist()
        last_date = df_prophet['ds'].max()
        future_dates = pd.date_range(start=last_date + pd.offsets.BDay(1), 
                                    periods=days_futuro, freq='B')  # Começa no próximo dia útil
        all_dates = historical_dates + future_dates.tolist()
        future = pd.DataFrame({'ds': all_dates})
        
        # Garantir que o número de dias úteis futuros seja suficiente
        future_futuro = future[future['ds'] > last_date]
        if len(future_futuro) < days_futuro:
            raise ValueError(f"Não foi possível gerar {days_futuro} dias úteis futuros. Gerados: {len(future_futuro)}")
        
        # Gerar previsões
        forecast = modelo.predict(future)
        
        # Alinhar previsões históricas com os dados reais usando merge
        forecast_historical = pd.merge(df_prophet[['ds']], forecast[['ds', 'yhat']], 
                                      on='ds', how='left')['yhat'].values
        y_true = df_prophet['y'].values
        
        if len(y_true) != len(forecast_historical):
            print(f"Datas históricas: {df_prophet['ds'].tolist()}")
            print(f"Datas previstas alinhadas: {forecast[forecast['ds'].isin(df_prophet['ds'])]['ds'].tolist()}")
            raise ValueError(f"Tamanhos incompatíveis após alinhamento: y_true ({len(y_true)}) e forecast_historical ({len(forecast_historical)}).")
        
        return {
            'forecast': forecast,
            'modelo': modelo,
            'r2': r2_score(y_true, forecast_historical),
            'mae': mean_absolute_error(y_true, forecast_historical),
            'ultima_previsao': forecast['yhat'].values[-1]
        }
    
    except Exception as e:
        print(f"Erro na função prever_preco_prophet: {str(e)}")
        return None