import pytest
import pandas as pd
from ml import prever_preco_prophet

class TestPreverPreçoProphet:
    """Testes para função prever_preco_prophet"""

    @pytest.fixture
    def sample_historical_data(self):
        """Dados históricos de exemplo"""
        dates = pd.date_range(start='2024-01-01', periods=90, freq='B')
        prices = [100 + i * 0.5 for i in range(90)]
        return pd.DataFrame({'date': dates, 'price': prices})

    def test_predict_success(self, sample_historical_data):
        """Testa predição bem-sucedida"""
        result = prever_preco_prophet(sample_historical_data, days_futuro=30)

        assert result is not None
        assert 'forecast' in result
        assert 'r2' in result
        assert 'mae' in result
        assert result['r2'] >= -1  # R² pode ser negativo em casos extremos

    def test_predict_missing_columns(self):
        """Testa erro com colunas faltando"""
        df_invalid = pd.DataFrame({'wrong_col': [1, 2, 3]})

        result = prever_preco_prophet(df_invalid)
        assert result is None

    def test_predict_empty_dataframe(self):
        """Testa erro com DataFrame vazio"""
        df_empty = pd.DataFrame({'date': [], 'price': []})

        result = prever_preco_prophet(df_empty)
        assert result is None
