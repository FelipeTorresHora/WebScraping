import pytest
import pandas as pd
from unittest.mock import Mock

@pytest.fixture
def sample_fii_dataframe():
    """Retorna DataFrame de exemplo com dados de FIIs"""
    return pd.DataFrame({
        'código': ['HGLG11', 'MXRF11'],
        'segmento': ['Logística', 'Híbrido'],
        'cotação': [150.50, 10.25],
        'dividend_yield': [8.5, 12.3],
        'p_vp': [0.95, 1.02],
        'valor_mercado': [1500000000, 2000000000],
        'liquidez': [5000000, 8000000],
        'qt_imoveis': [25, 150],
        'vacancia': [5.2, 3.8]
    })

@pytest.fixture
def mock_requests_get(monkeypatch):
    """Mock para requests.get"""
    mock = Mock()
    mock.status_code = 200
    monkeypatch.setattr('requests.get', lambda *args, **kwargs: mock)
    return mock
