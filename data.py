import requests
from bs4 import BeautifulSoup
import locale
import pandas as pd

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

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
                cotacao = locale.atof(dados_fundo[2].text.split()[0])
                dy = locale.atof(dados_fundo[4].text.split('%')[0])
                
                if cotacao <= 3000 and dy <= 300:
                    dados.append({
                        'código': dados_fundo[0].text,
                        'segmento': dados_fundo[1].text,
                        'cotação': cotacao,
                        'dividend_yield': dy,
                        'p_vp': locale.atof(dados_fundo[5].text.split()[0]),
                        'valor_mercado': locale.atof(dados_fundo[6].text.split()[0]),
                        'liquidez': locale.atof(dados_fundo[7].text.split()[0]),
                        'qt_imoveis': int(dados_fundo[8].text),
                        'vacancia': locale.atof(dados_fundo[12].text.split('%')[0])
                    })
    except Exception as e:
        raise Exception(f"Erro ao obter dados: {str(e)}")
    
    return pd.DataFrame(dados)