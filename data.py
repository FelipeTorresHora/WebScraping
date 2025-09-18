import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
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
    headers = {"User-Agent": "Mozilla/5.0"}
    resposta = requests.get('https://fundamentus.com.br/fii_resultado.php', headers=headers)
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
                
                if cotacao <= 3000 and dy <= 300:
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
    except Exception as e:
        raise Exception(f"Erro ao obter dados: {str(e)}")
    
    return pd.DataFrame(dados)

def get_historical_data(ticker):
    token = os.getenv("BRAPI_TOKEN")
    url = f"https://brapi.dev/api/quote/{ticker}?range=3mo&interval=1d&fundamental=false&token={token}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
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