import pytest
from data import parse_brazilian_number

class TestParseBrazilianNumber:
    """Testes para função parse_brazilian_number"""

    def test_parse_standard_format(self):
        """Testa parsing de formato padrão 1.234,56"""
        assert parse_brazilian_number("1.234,56") == 1234.56

    def test_parse_zero(self):
        """Testa parsing de zero"""
        assert parse_brazilian_number("0,00") == 0.0

    def test_parse_large_number(self):
        """Testa parsing de número grande"""
        assert parse_brazilian_number("1.500.000,00") == 1500000.0

    def test_parse_decimal_only(self):
        """Testa parsing de apenas decimais"""
        assert parse_brazilian_number("0,75") == 0.75

    def test_parse_invalid_string(self):
        """Testa parsing de string inválida"""
        assert parse_brazilian_number("abc") == 0.0

    def test_parse_empty_string(self):
        """Testa parsing de string vazia"""
        assert parse_brazilian_number("") == 0.0

    def test_parse_with_extra_spaces(self):
        """Testa parsing com espaços extras"""
        assert parse_brazilian_number("  1.234,56  ") == 1234.56
