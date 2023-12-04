import requests
from bs4 import BeautifulSoup

#header necessário para que o servidor entenda que estamos buscando informações no servidor.
headers = {"User-Agent" : "Mozilla/5.0"} 
resposta = requests.get('https://fundamentus.com.br/fii_resultado.php', headers = headers)
soup = BeautifulSoup(resposta.text, 'html.parser')
linhas = soup.find(id='tabelaResultado').find('tbody').find_all('tr')

for linha in linhas:
    dados_fundo = linha.find_all('td')
    
    codigo = dados_fundo[0].text
    segmento = dados_fundo[1].text
    cotacao_atual = dados_fundo[2].text
    ffo_yield = dados_fundo[3].text
    dividend_yield = dados_fundo[4].text
    p_vp = dados_fundo[5].text
    valor_mercado = dados_fundo[6].text
    liquidez = dados_fundo[7].text
    qt_imoveis = dados_fundo[8].text
    preco_m2 = dados_fundo[9].text
    aluguel_m2 = dados_fundo[10].text
    cap_rate = dados_fundo[11].text
    vacancia_media = dados_fundo[12].text