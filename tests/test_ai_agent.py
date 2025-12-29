import pytest
from unittest.mock import patch, Mock
import os
from ai_agent import GeminiAgent, analyze_fii_with_ai

class TestGeminiAgent:
    """Testes para classe GeminiAgent"""

    @patch.dict(os.environ, {'gemini_api': 'fake_key'})
    @patch('ai_agent.genai.GenerativeModel')
    def test_init_success(self, mock_model):
        """Testa inicialização bem-sucedida"""
        agent = GeminiAgent()
        assert agent.api_key == 'fake_key'

    def test_init_missing_api_key(self):
        """Testa erro quando API key está faltando"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError):
                GeminiAgent()

    @patch.dict(os.environ, {'gemini_api': 'fake_key'})
    @patch('ai_agent.genai.GenerativeModel')
    def test_get_response_success(self, mock_model):
        """Testa resposta bem-sucedida do modelo"""
        mock_chat = Mock()
        mock_response = Mock()
        mock_response.text = "Análise do FII"
        mock_chat.send_message.return_value = mock_response

        mock_instance = Mock()
        mock_instance.start_chat.return_value = mock_chat
        mock_model.return_value = mock_instance

        agent = GeminiAgent()
        response = agent.get_response("Análise HGLG11")

        assert response == "Análise do FII"

class TestAnalyzeFiiWithAi:
    """Testes para função analyze_fii_with_ai"""

    @patch('ai_agent.GeminiAgent')
    @patch('ai_agent.obter_dados_fiis')
    def test_analyze_fii_success(self, mock_obter_dados, mock_agent_class,
                                 sample_fii_dataframe):
        """Testa análise bem-sucedida de FII"""
        mock_obter_dados.return_value = sample_fii_dataframe

        mock_agent = Mock()
        mock_agent.api_key = 'fake_key'
        mock_agent.get_response.return_value = "Análise positiva"
        mock_agent_class.return_value = mock_agent

        result = analyze_fii_with_ai('HGLG11')

        assert result == "Análise positiva"
        mock_agent.get_response.assert_called_once()

    @patch('ai_agent.GeminiAgent')
    @patch('ai_agent.obter_dados_fiis')
    def test_analyze_fii_not_found(self, mock_obter_dados, mock_agent_class,
                                   sample_fii_dataframe):
        """Testa análise de FII não encontrado"""
        mock_obter_dados.return_value = sample_fii_dataframe

        mock_agent = Mock()
        mock_agent.api_key = 'fake_key'
        mock_agent_class.return_value = mock_agent

        result = analyze_fii_with_ai('XXXXX11')

        assert "não encontrado" in result
