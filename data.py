import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import os
from logger_config import setup_logger
from constants import HTTP_TIMEOUT, MAX_VALID_COTACAO, MAX_VALID_DIVIDEND_YIELD, USER_AGENT

load_dotenv()
logger = setup_logger(__name__)
def parse_brazilian_number(text):
    """
    Converte número no formato brasileiro para float.
    Exemplo: "1.234,56" -> 1234.56
    """
    # Remove espaços e converte vírgula para ponto, remove pontos de milhar
    cleaned = text.replace('.', '').replace(',', '.').strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

@st.cache_data
def obter_dados_fiis():
    """
    Obtém dados de FIIs do site Fundamentus através de web scraping.

    Realiza scraping da tabela de FIIs do Fundamentus, parseando os valores
    em formato brasileiro e filtrando outliers baseado em limites predefinidos.

    Returns:
        pd.DataFrame: DataFrame com colunas:
            - código: Código do FII (ex: HGLG11)
            - segmento: Segmento de atuação
            - cotação: Preço atual em R$
            - dividend_yield: Dividend yield em %
            - p_vp: Preço sobre valor patrimonial
            - valor_mercado: Valor de mercado em R$
            - liquidez: Liquidez diária em R$
            - qt_imoveis: Quantidade de imóveis
            - vacancia: Taxa de vacância em %

    Raises:
        ConnectionError: Erro na requisição HTTP ao Fundamentus
        ValueError: Erro ao parsear a estrutura HTML
    """
    headers = {"User-Agent": USER_AGENT}
    resposta = requests.get('https://fundamentus.com.br/fii_resultado.php',
                           headers=headers, timeout=HTTP_TIMEOUT)
    soup = BeautifulSoup(resposta.text, 'html.parser')
    
    dados = []
    try:
        tabela = soup.find(id='tabelaResultado')
        if tabela and tabela.find('tbody'):
            linhas = tabela.find('tbody').find_all('tr')
            for linha in linhas:
                dados_fundo = linha.find_all('td')
                cotacao = parse_brazilian_number(dados_fundo[2].text.split()[0])
                dy = parse_brazilian_number(dados_fundo[4].text.split('%')[0])

                # Filtrar outliers usando constantes
                if cotacao <= MAX_VALID_COTACAO and dy <= MAX_VALID_DIVIDEND_YIELD:
                    dados.append({
                        'código': dados_fundo[0].text,
                        'segmento': dados_fundo[1].text,
                        'cotação': cotacao,
                        'dividend_yield': dy,
                        'p_vp': parse_brazilian_number(dados_fundo[5].text.split()[0]),
                        'valor_mercado': parse_brazilian_number(dados_fundo[6].text.split()[0]),
                        'liquidez': parse_brazilian_number(dados_fundo[7].text.split()[0]),
                        'qt_imoveis': int(dados_fundo[8].text),
                        'vacancia': parse_brazilian_number(dados_fundo[12].text.split('%')[0])
                    })
    except requests.RequestException as e:
        logger.error(f"Erro de requisição ao Fundamentus: {e}")
        raise ConnectionError(f"Falha ao buscar dados de FIIs: {str(e)}") from e
    except AttributeError as e:
        logger.error(f"Erro ao parsear HTML do Fundamentus: {e}")
        raise ValueError(f"Estrutura HTML inesperada: {str(e)}") from e
    except Exception as e:
        logger.critical(f"Erro inesperado em obter_dados_fiis: {e}")
        raise
    
    return pd.DataFrame(dados)

def get_historical_data(ticker):
    """
    Obtém dados históricos de preços de um FII via API BRAPI.

    Args:
        ticker (str): Código do FII (ex: HGLG11)

    Returns:
        pd.DataFrame: DataFrame com colunas 'date' e 'price', ou None em caso de erro

    Note:
        Retorna últimos 3 meses de dados históricos (intervalo diário)
    """
    token = os.getenv("BRAPI_TOKEN")
    url = f"https://brapi.dev/api/quote/{ticker}?range=3mo&interval=1d&fundamental=false&token={token}"
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)
    
    if response.status_code != 200:
        st.warning(f"Erro na requisição à Brapi para {ticker}: Status {response.status_code} - {response.text}")
        return None
    
    data = response.json()
    if "results" not in data or not data["results"]:
        st.warning(f"Sem dados históricos para {ticker}. Resposta da API: {data}")
        return None
    
    try:
        historical = data["results"][0]["historicalDataPrice"]
        df = pd.DataFrame(historical)
        df["date"] = pd.to_datetime(df["date"], unit="s")
        df = df[["date", "close"]].rename(columns={"close": "price"})
        return df
    except KeyError as e:
        st.warning(f"Erro no formato dos dados retornados para {ticker}: {str(e)}. Resposta: {data}")
        return None