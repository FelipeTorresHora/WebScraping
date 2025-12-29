import pytest
from unittest.mock import patch, Mock, MagicMock
import os
from envio import enviar_email, gerar_pdf_relatorio

class TestEnviarEmail:
    """Testes para função enviar_email"""

    @patch('envio.smtplib.SMTP')
    @patch.dict(os.environ, {'SENDER_EMAIL': 'test@example.com',
                             'Senha_Email': 'password'})
    def test_enviar_email_success(self, mock_smtp):
        """Testa envio bem-sucedido de email"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        result = enviar_email('dest@example.com', 'Assunto', 'Corpo')

        assert result is True
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        mock_server.sendmail.assert_called_once()

    @patch('envio.smtplib.SMTP')
    def test_enviar_email_missing_env_var(self, mock_smtp):
        """Testa erro quando variável de ambiente está faltando"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError):
                enviar_email('dest@example.com', 'Assunto', 'Corpo')

class TestGerarPdfRelatorio:
    """Testes para função gerar_pdf_relatorio"""

    def test_gerar_pdf_success(self, sample_fii_dataframe, tmp_path):
        """Testa geração bem-sucedida de PDF"""
        filtros = {"Cotação Mínima": 100}
        output_file = tmp_path / "test_report.pdf"

        result = gerar_pdf_relatorio(filtros, sample_fii_dataframe,
                                     nome_arquivo=str(output_file))

        assert result == str(output_file)
        assert output_file.exists()
